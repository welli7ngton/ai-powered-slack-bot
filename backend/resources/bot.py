from flask_restful import Resource
from flask import jsonify

from services.bot_service import BotService


class Bot(Resource):
    __service__ = BotService()

    def post(self, message, channel):
        try:
            response = self.__service__.send_message(message, channel)
            if response:
                return jsonify({"message": f"Message '{message}' sent to channel {channel}."}), 200
        except Exception as e:
            return jsonify({"error": f"An error occured: {e}"}), 500
