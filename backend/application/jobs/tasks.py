import time
from json import dumps

from httplib2 import Http

from application.data.models import List, User
from application.jobs.workers import celery
from datetime import datetime

from celery.schedules import crontab
print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(10.0, print_current_time_job.s(), name='add every 10')
    pass


def pending_tasks():
    lists = List.query.all()
    response = {}
    text = ''
    for list in lists:
        cards = list.cards
        for card in cards:
            if not card.completed and card.deadline < datetime.now():
                delay = datetime.now() - card.deadline
                (hours, mins) = (str(delay).split(':')[0], str(delay).split(':')[1])
                text += "card {}, delayed by: {} hours, {} minutes \n".format(card.title, hours, mins)
                # delay = datetime.now() - card.deadline
                # text += "card {}, delayed by: {}, ".format(card.title, str(delay))

    response['text'] = text
    print("response", response)
    return response


def monthly_report():
    users = User.query.all()
    response = {}
    final_response = ''
    for user in users:
        final_response += user.username + "\n"
        lists = user.lists

        for list in lists:

            cards = list.cards
            list_data = {'finished_in_time': 0, 'late_completion': 0,
                         'pending': 0, 'backlog': 0}
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
            final_response += '{} status - Finished: {}, Late: {}, Pending: {}, Backlog: {} \n'\
                .format(list.name, list_data['finished_in_time'],
                        list_data['late_completion'], list_data['pending'],
                        list_data['backlog'])
            final_response += '\n'
    response['text'] = final_response
    return response


@celery.task
def google_chat_monthly():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'https://chat.googleapis.com/v1/spaces/AAAArEWsc6g/messages?key=AIzaSy' \
          'DdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=IwO0bbS0olwnGw0l1dsVYaGqqrdnYyYJYq96Y6ZbBjA%3D'

    bot_message = monthly_report()
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )


@celery.task
def google_chat_daily():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'https://chat.googleapis.com/v1/spaces/AAAArEWsc6g/messages?key=AIzaSy' \
          'DdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=IwO0bbS0olwnGw0l1dsVYaGqqrdnYyYJYq96Y6ZbBjA%3D'

    bot_message = pending_tasks()
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)
