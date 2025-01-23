from os import environ
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse


class BotService:
    __username__ = 'ask-me'

    def __init__(self):
        load_dotenv()
        self.client = WebClient(environ['APP_OAUTH_TOKEN'])
        self.secret = environ['SLACK_CLIENT_SECRET']

    def send_message(self, message: str, channel_name: str, thread_ts: str) -> SlackResponse:
        try:
            # TODO: Handle response
            self.client.chat_postMessage(
                channel=channel_name,
                text=message,
                thread_ts=thread_ts,
                as_user=self.__username__
            )
            return {"test": "test post request."}
        except SlackApiError as e:
            raise Exception(e.response['error'])
