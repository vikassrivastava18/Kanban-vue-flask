import datetime

from flask_restful import Resource
from flask_restful import reqparse

from application.data.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, make_response, jsonify
from datetime import datetime, timedelta


from application.data.models import User, TokenLogout, Card, List

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')

login_user_parser = reqparse.RequestParser()
login_user_parser.add_argument('email')
login_user_parser.add_argument('password')

user_info_parser = reqparse.RequestParser()
user_info_parser.add_argument('token')

change_list_parser = reqparse.RequestParser()
change_list_parser.add_argument('list_id')
change_list_parser.add_argument('card_id')


create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('name')


create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('title')
create_card_parser.add_argument('content')
create_card_parser.add_argument('deadline')
create_card_parser.add_argument('listId')

edit_card_parser = reqparse.RequestParser()
edit_card_parser.add_argument('title')
edit_card_parser.add_argument('content')
edit_card_parser.add_argument('deadline')
edit_card_parser.add_argument('completed')


class CardResource(Resource):

    def post(self):
        auth_token = request.headers.get('Authorization')
        args = create_card_parser.parse_args()
        print("args", args)
        card_title = args.get("title", None)
        card_content = args.get("content", None)
        deadline = args.get("deadline", None)
        listId = args.get("listId", None)
        print(card_title, card_content, deadline)

        if check_token_valid(auth_token):
            user_id = User.decode_jwt_token(auth_token)
            card = Card(title=card_title, content=card_content,
                        deadline=datetime.now() + timedelta(days=0, seconds=3600 * int(deadline)),
                        list=int(listId))
            db.session.add(card)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully created list.',
            }
            return make_response(jsonify(responseObject), 201)
        responseObject = {
            'status': 'fail',
            'message': 'Authentication error'
        }
        return make_response(jsonify(responseObject), 401)

    def get(self, card_id):
        auth_token = request.headers.get('Authorization')
        if check_token_valid(auth_token):
            card = Card.query.filter_by(card_id=card_id).first()
            response = {
                'status': 'Success',
                'card': card
            }
            return make_response(jsonify(response), 200)

        else:
            response = {
                'status': 'fail',
                'message': 'Authentication error',
            }
            return make_response(jsonify(response), 401)

    def put(self, card_id):
        auth_token = request.headers.get('Authorization')

        if check_token_valid(auth_token):
            card = Card.query.filter_by(card_id=card_id).first()
            args = edit_card_parser.parse_args()
            card.title = args.get("title", None)
            card.content = args.get("content", None)
            completed = args.get("completed", None)
            deadline = args.get("deadline", None)
            try:
                if not int(deadline) == 0:
                    card.deadline = datetime.now() + timedelta(days=0, seconds=3600 * int(deadline))
            except:
                pass
            print("completed", completed)
            if completed == "True" or completed == "true":
                print("completed!@#$")
                card.completed = True
                card.completed_on = datetime.now()
            else:
                card.completed = False

            db.session.commit()
            print("status", card.completed)
            response = {
                'status': 'Success',
                'message': 'Card updated successfully'
            }

            return make_response(jsonify(response), 200)

        else:
            response = {
                'status': 'fail',
                'message': 'Authentication error',
            }
            return make_response(jsonify(response), 401)

    def delete(self, card_id):
        auth_token = request.headers.get('Authorization')
        print(card_id)

        if check_token_valid(auth_token):
            Card.query.filter_by(card_id=card_id).delete()
            db.session.commit()

            response = {
                'status': 'Success',
                'message': 'Card removed'
            }
            return make_response(jsonify(response), 200)


class RegisterAPI(Resource):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)
        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
        if not user:
            try:
                user = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password)
                )

                # insert the user
                db.session.add(user)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
                return make_response(jsonify(responseObject), 201)
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'error': str(e)
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'error': 'User already exists. Please change credentials',
            }
            return make_response(jsonify(responseObject), 202)


class LoginApi(Resource):
    """
    User login API
    """

    def post(self):
        # get the post data
        args = login_user_parser.parse_args()
        email = args.get("email", None)
        password = args.get("password", None)
        print(email, password)
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            try:
                auth_token = user.encode_jwt_token()
                if auth_token:
                    response = {
                        'status': 'Success',
                        'message': 'Logged in',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response), 200)
                else:
                    response = {
                        'status': 'failed',
                        'message': 'User does not exist.'
                    }
                    return make_response(jsonify(response), 404)
            except Exception as e:
                print("error", e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject, 401))
        else:
            response = {
                'status': 'fail',
                'message': 'Credentials invalid, please try with right credentials',
            }
            return make_response(jsonify(response), 202)


class LogoutApi(Resource):
    def get(self):
        # TODO
        pass


class ListReportResource(Resource):
    """
    Get all the cards' Reposrt for a list
    """

    def get(self, list_id):
        auth_token = request.headers.get('Authorization')
        if check_token_valid(auth_token):
            user_id = User.decode_jwt_token(auth_token)
            list = List.query.filter_by(user=user_id).filter_by(list_id=list_id).first()
            response = []
            cards = list.cards
            list_data = {'finished_in_time': 0, 'late_completion': 0,
                         'pending': 0, 'backlog': 0,
                         'list': list.name}
            for card in cards:
                try:
                    if card.completed and card.completed_on <= card.deadline:
                        list_data['finished_in_time'] += 1
                    elif card.completed and card.completed_on > card.deadline:
                        list_data['late_completion'] += 1
                    elif not card.completed and card.deadline < datetime.now():
                        list_data['backlog'] += 1
                    else:
                        list_data['pending'] += 1
                except Exception as e:
                    continue

            response.append(list_data['finished_in_time'])
            response.append(list_data['late_completion'])
            response.append(list_data['pending'])
            response.append(list_data['backlog'])
            response.append(list_data['list'])
            return make_response(jsonify(response), 200)

        else:
            response = {
                'status': 'fail',
                'message': 'Credentials invalid, please try with right credentials',
            }
            return make_response(jsonify(response), 202)


def check_logout(token):
    token = TokenLogout.query.filter_by(token=token).first()
    if token:
        return True
    return False


class UserListCardResource(Resource):
    """
    return users lists and cards info
    """
    def get(self):
        auth_token = request.headers.get('Authorization')
        print("auth token", auth_token)

        response = []
        if check_token_valid(auth_token):
            print("valid")
            user_id = User.decode_jwt_token(auth_token)
            user = User.query.filter_by(user_id=user_id).first()
            lists = user.lists
            lists_data = [[list.list_id, list.name] for list in lists]
            response.append({'lists': lists_data})
            for list in lists:
                for card in list.cards:
                    list_data = {}
                    list_data['list'] = list.name
                    list_data['list_id'] = list.list_id
                    list_data['card_id'] = card.card_id
                    list_data['title'] = card.title
                    list_data['content'] = card.content
                    list_data['deadline'] = card.deadline.strftime("%m/%d/%Y, %H:%M:%S")
                    list_data['completed'] = card.completed
                    response.append(list_data)
            print("response", response)
            return make_response(jsonify(response), 200)
        else:
            response = {
                'status': 'fail',
                'message': 'Credentials invalid, please try with right credentials',
            }
            return make_response(jsonify(response), 202)


class ChangeListCards(Resource):
    """
    return users lists and cards info
    """
    def post(self):
        print("changing!@#")
        auth_token = request.headers.get('Authorization')
        args = change_list_parser.parse_args()
        list_id = args.get("list_id")
        card_id = args.get("card_id")
        # print("list id", list_id, "card id", card_id)
        if check_token_valid(auth_token):
            # card = data_access.get_card(card_id)
            card = Card.query.filter_by(card_id=card_id).first()
            card.list = list_id
            db.session.commit()

            response = {
                'status': 'Success',
                'message': 'List updated',
            }

            return make_response(jsonify(response), 200)

        else:
            response = {
                'status': 'fail',
                'message': 'Credentials invalid, please try with right credentials',
            }
            return make_response(jsonify(response), 202)


class ListResource(Resource):
    def post(self):
        auth_token = request.headers.get('Authorization')
        args = create_list_parser.parse_args()
        list_name = args.get("name", None)

        if check_token_valid(auth_token):
            user_id = User.decode_jwt_token(auth_token)
            list = List(name=list_name, user=user_id)
            db.session.add(list)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully created list.',
            }
            return make_response(jsonify(responseObject), 201)
        responseObject = {
            'status': 'fail',
            'message': 'Authentication error'
        }
        return make_response(jsonify(responseObject), 401)

    def put(self, name):
        args = create_list_parser.parse_args()
        list = List.query.filter_by(name=name).first()
        list_name = args.get("name", None)
        list.name = list_name
        db.session.add(list)
        db.session.commit()
        response = {
            'status': 'Success',
            'message': 'List updated successfully'
        }

        return make_response(jsonify(response), 200)

    def delete(self, name):
        list = List.query.filter_by(name=name).first()
        for card in list.cards:
            Card.query.filter_by(card_id=card.card_id).delete()
        db.session.commit()
        List.query.filter_by(name=name).delete()
        db.session.commit()
        response = {
            'status': 'Success',
            'message': 'List deleted successfully'
        }

        return make_response(jsonify(response), 200)


from application.data import data_access


def check_token_valid(token):
    try:
        user_id = User.decode_jwt_token(token)
        # Cached user data
        # user = data_access.get_user(str(user_id))
        user = User.query.filter_by(user_id=user_id).first()
        print("user", user)
        if user:
            return True
    except Exception as e:
        return False


