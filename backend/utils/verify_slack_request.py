import hashlib
import hmac
import time


def verify_slack_request(req, slack_signing_secret):
    timestamp = req.headers.get('X-Slack-Request-Timestamp')
    if not timestamp or abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    req_data = req.get_data(as_text=True)
    print("request data", req_data)

    sig_basestring = f"v0:{timestamp}:{req_data}"
    my_signature = 'v0=' + hmac.new(
        slack_signing_secret,
        sig_basestring,
        hashlib.sha256
    ).hexdigest()

    slack_signature = req.headers.get('x-slack-signature')
    print(f"Timestamp: {timestamp}")
    print(f"Base String: {sig_basestring}")
    print(f"My Sig: {my_signature}")
    print(f"Slack Sig: {slack_signature}")
    return hmac.compare_digest(my_signature, slack_signature)
