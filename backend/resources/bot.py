import redis

from time import sleep
from slack_sdk.errors import SlackApiError
from flask_restful import Resource
from flask import jsonify, make_response, request

from services.bot_service import BotService
from services.llm_service import LLMService
from utils.verify_slack_request import verify_slack_request

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=0)

class BotAnswerMessage(Resource):
    __service__ = BotService()
    __llm_service__ = LLMService()

    def post(self):
        if not verify_slack_request(request, self.__service__.secret):
            return make_response("Invalid request signature.", 403)

        data = request.json

        # URL Verification Challenge
        if data.get("type") == "url_verification":
            
            return jsonify({"challenge": data.get("challenge")})

        if data.get("type") == "event_callback":
            event_id = data.get("event_id")
            if REDIS_CLIENT.get(event_id):
                sleep(2)
                return make_response("", 200)
            
            REDIS_CLIENT.set(event_id, "processed", ex=300)
            
            event = data.get("event", {})
            if event.get("type") == "app_mention":
                text = event.get("text")
                channel = event.get("channel")

                try:
                    response_text = self.__llm_service__.ask_question(text)
                    sleep(2)
                    # TODO: Handle response
                    self.__service__.send_message(
                        message=response_text, channel_name=channel
                    )
                    return make_response("", 200)

                except SlackApiError as e:
                    print(f"Error sending message: {e.response['error']}")
        return make_response("", 200)
