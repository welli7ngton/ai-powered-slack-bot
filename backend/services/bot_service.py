from os import environ
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class BotService:
    def __init__(self):
        load_dotenv()
        self.client = self._initialize_client()
        self.secret = environ.get("SLACK_SIGNING_SECRET")
        if not self.secret:
            raise ValueError("SLACK_SIGNING_SECRET is not set in the environment variables.")

    def _initialize_client(self) -> WebClient:
        # Initializes the Slack WebClient with the app's OAuth token.
        app_oauth_token = environ.get("APP_OAUTH_TOKEN")
        if not app_oauth_token:
            raise ValueError("APP_OAUTH_TOKEN is not set in the environment variables.")
        
        return WebClient(token=app_oauth_token)

    def send_message(
        self, message: str, channel_name: str, *, thread_ts: str | None = None
    ) -> dict:
        """
        Sends a message to a Slack channel.

        Args:
            message (str): The message to send.
            channel_name (str): The Slack channel where the message will be sent.
            thread_ts (str | None, optional): The thread timestamp for threading messages. Defaults to None.

        Returns:
            dict: Response data from the Slack API.

        Raises:
            Exception: If the Slack API call fails.
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel_name,
                text=message,
                thread_ts=thread_ts,
                as_user=True
            )
            return {"status": "success", "data": response.data}

        except SlackApiError as e:
            error_message = f"Error sending message: {e.response.get('error', 'Unknown error')}"
            raise Exception(error_message)
