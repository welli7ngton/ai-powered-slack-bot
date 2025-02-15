import sys
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

sys.path = sys.path + ["./backend"]

from resources.home import Home
from resources.auth import SlackAuth
from resources.bot import BotAnswerMessage

load_dotenv()


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Home, "/")
    api.add_resource(SlackAuth, "/auth")
    api.add_resource(BotAnswerMessage, "/slack/events")

    return app
