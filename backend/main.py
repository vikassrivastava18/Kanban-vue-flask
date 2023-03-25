import csv
import os

from celery.schedules import crontab
from flask import Flask
from flask_restful import Resource, Api
from application.config import LocalDevelopmentConfig, StageConfig
from application.data.database import db
from application.data.models import List
from application.jobs import workers
from flask_cors import CORS

from flask_caching import Cache

from application.jobs.tasks import google_chat_daily, google_chat_monthly


def create_app():
    app = Flask(__name__, template_folder="templates")

    # print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      app.logger.info("Staring stage.")
      app.config.from_object(StageConfig)
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    app.app_context().push()
    print("DB Init")
    with app.app_context():
        db.init_app(app)
    print("DB Init complete")
    app.app_context().push()
    app.logger.info("App setup complete")

    api = Api(app)
    app.app_context().push()

    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    cache = Cache(app)
    app.app_context().push()

    print("Create app complete")
    return app, api, celery, cache


app, api, celery, cache = create_app()
CORS(app)


# # Add all restful controllers
from application.controller.api import CardResource
api.add_resource(CardResource,  "/api/card", "/api/card/<int:card_id>")

from application.controller.api import RegisterAPI
api.add_resource(RegisterAPI, "/api/register")

from application.controller.api import LoginApi
api.add_resource(LoginApi, "/api/login")

from application.controller.api import UserListCardResource
api.add_resource(UserListCardResource, "/api/token-test")

from application.controller.api import ChangeListCards
api.add_resource(ChangeListCards, "/api/change-list")

from application.controller.api import ListResource
api.add_resource(ListResource, "/api/create-list", "/api/edit-list/<name>", "/api/delete-list/<name>")

from application.controller.api import ListReportResource
api.add_resource(ListReportResource, "/api/list-report/<int:list_id>")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=14),
        google_chat_daily().s(),
    )


@celery.on_after_configure.connect
def setup_monthly_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=14, day_of_month=27),
        google_chat_monthly().s(),
    )


@app.route('/api/import-csv/<int:list_id>', methods=['POST'])
def download_report_csv(list_id):
    # Create the csv file in assets folder
    list = List.query.filter_by(list_id=list_id).first()
    cards = list.cards
    headers = ['Tile', 'Deadline', 'Completed', 'Completed on']
    rows = []
    for card in cards:
        row_data = []
        row_data.append(card.title)
        row_data.append(card.deadline.strftime("%m/%d/%Y, %H:%M:%S"))
        row_data.append(card.completed)
        row_data.append(card.completed_on)
        rows.append(row_data)
        filename = "assets/report.csv"

        # writing to csv file
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(rows)
    # Send it to the client
    f = open('assets/report.csv', 'rb')
    return f.read()


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0', port=8080)
