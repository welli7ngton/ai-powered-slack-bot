from os import environ
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse


class BotService:
    def __init__(self):
        load_dotenv()
        self.client = WebClient(environ['APP_OAUTH_TOKEN'])

    def send_message(self, message: str, channel_name: str) -> SlackResponse:
        try:
            response = self.client.chat_postMessage(channel=channel_name, text=message)
            return {"test": "test post request."}
        except SlackApiError as e:
            raise e.response['error']
