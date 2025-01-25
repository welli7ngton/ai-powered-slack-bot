import redis

from time import sleep
from slack_sdk.errors import SlackApiError
from flask_restful import Resource
from flask import jsonify, make_response, request

from services.bot_service import BotService
from services.llm_service import LLMService
from utils.verify_slack_request import verify_slack_request

# Improved Redis connection with better configuration
REDIS_CLIENT = redis.StrictRedis(
    host="172.17.0.1",
    port=6379,
    db=0,
    decode_responses=True,  # Ensure values are decoded as strings
)


class BotAnswerMessage(Resource):
    __service__ = BotService()
    __llm_service__ = LLMService()

    def post(self):
        # Verify Slack request signature
        if not verify_slack_request(request, self.__service__.secret):
            return make_response("Invalid request signature.", 403)

        data = request.json

        if data.get("type") == "url_verification":
            return jsonify({"challenge": data.get("challenge")})

        if data.get("type") == "event_callback":
            event_id = data.get("event_id")
            event = data.get("event", {})

            # Prevent processing duplicate events using Redis with better expiration
            if not REDIS_CLIENT.set(event_id, "processed", ex=300, nx=True):  # `nx=True` ensures the key is set only if it doesn't exist
                return make_response("", 200)

            if event.get("type") == "app_mention":
                text = event.get("text")
                channel = event.get("channel")
                return self._handle_app_mention(text, channel)

        return make_response("", 200)

    def _handle_app_mention(self, text, channel):      
        # Handles messages where the bot is mentioned.
        try:
            # Query the LLM service for a response
            response_text = self.__llm_service__.ask_question(text)
            sleep(2)

            # Send the response to the specified Slack channel
            self.__service__.send_message(
                message=response_text, channel_name=channel
            )
            return make_response("", 200)

        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
            return make_response("Internal Server Error", 500)
