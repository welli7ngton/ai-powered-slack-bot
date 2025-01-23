import sys
import os
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


if __name__ == '__main__':
    cert_path = os.getenv("CERT_PATH")
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=(f'{cert_path}cert.pem', f'{cert_path}key.pem'))
