from flask import request, jsonify, redirect
from flask_restful import Resource
import os
import urllib3
import json


class SlackAuth(Resource):
    def __init__(self):
        self.client_id = os.getenv("SLACK_CLIENT_ID")
        self.client_secret = os.getenv("SLACK_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SLACK_REDIRECT_URI")
        self.oauth_url = "https://slack.com/oauth/v2/authorize"
        self.token_url = "https://slack.com/api/oauth.v2.access"
        self.http = urllib3.PoolManager()

    def get(self):
        """
        Initiates Slack OAuth 2.0 flow by redirecting the user to Slack's authorization URL.
        """
        if not self.client_id or not self.redirect_uri:
            return jsonify({"error": "Slack credentials are not set"}), 500

        # Build Slack OAuth URL
        slack_url = (
            f"{self.oauth_url}?client_id={self.client_id}"
            f"&scope=chat:write,commands,im:history,im:write"
            f"&redirect_uri={self.redirect_uri}"
        )
        return redirect(slack_url)

    def post(self):
        """
        Handles the callback from Slack and exchanges the code for an access token.
        """
        auth_code = request.json.get("code")

        if not auth_code:
            return jsonify({"error": "Missing 'code' parameter in the request"}), 400

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
        }

        encoded_data = urllib3.request.urlencode(payload)

        response = self.http.request_encode_body(
            "POST",
            self.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=encoded_data,
        )

        # Parse response
        if response.status != 200:
            return jsonify({"error": "Failed to exchange code for token"}), 500

        data = json.loads(response.data.decode("utf-8"))
        if not data.get("ok"):
            return jsonify({"error": data.get("error", "Unknown error")}), 500

        return jsonify(
            {
                "access_token": data.get("access_token"),
                "team_id": data.get("team", {}).get("id"),
                "team_name": data.get("team", {}).get("name"),
                "bot_user_id": data.get("bot_user_id"),
            }
        )
