import sys
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from .routes.routes import Home
from .routes.auth import SlackAuth

sys.path = sys.path + ["./backend"]
load_dotenv()


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Home, "/")
    api.add_resource(SlackAuth, "/auth")

    return app
