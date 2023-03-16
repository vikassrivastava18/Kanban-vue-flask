from datetime import datetime, timedelta
import jwt
from application.data.database import db
from application.config import Config as conf # Note 


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    lists = db.relationship("List", backref='user_obj')

    def __repr__(self):
        return f'<User "{self.username}">'

    def encode_jwt_token(self):
        """
        Create the payload using the User id
        Add token creation/expiration timestamps
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, hours=1),
                'iat': datetime.utcnow(),
                'sub': self.user_id
            }
            return jwt.encode(
                payload,
                conf.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print("error", e)
            return e

    @staticmethod
    def decode_jwt_token(auth_token):
        """
        Decode the auth token, using the secret key
        return the user id if valid
        else raise expired/invalid token error
        """
        try:
            print("jwt token", auth_token)
            payload = jwt.decode(auth_token, conf.SECRET_KEY)
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature has expired, please try to login again '
        except jwt.InvalidTokenError:
            return 'Token is invalid, check credentials'


class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=False)
    user = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    cards = db.relationship("Card", backref='list_obj')

    def __repr__(self):
        return f'<List "{self.name}">'


class Card(db.Model):
    __tablename__ = "card"
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list = db.Column(db.Integer, db.ForeignKey("list.list_id"), nullable=False)
    title = db.Column(db.String, unique=False)
    content = db.Column(db.String, unique=False)
    deadline = db.Column(db.DateTime, index=True, default=datetime.utcnow() + timedelta(days=0, hours=6))
    completed = db.Column(db.Boolean(), default=False)
    completed_on = db.Column(db.DateTime)


class TokenLogout(db.Model):
    __tablename__ = 'token_logout'
    token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    logout_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id: token: {}'.format(self.token)





