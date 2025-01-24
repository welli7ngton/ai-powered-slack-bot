import hashlib
import hmac
import time


def verify_slack_request(request, slack_signing_secret):
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    if not timestamp or abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    req_data = request.get_data(as_text=True)

    sig_basestring = f"v0:{timestamp}:{req_data}"
    my_signature = (
        "v0="
        + hmac.new(
            slack_signing_secret.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    )

    slack_signature = request.headers.get("x-slack-signature")
    return hmac.compare_digest(my_signature, slack_signature)
