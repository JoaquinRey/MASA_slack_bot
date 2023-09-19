import sys
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient

logging.basicConfig(level=logging.DEBUG)

SOFTWARE_CHANNEL = ""
WEBHOOK_URL = ""

webhook = WebhookClient(WEBHOOK_URL)
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
api_response = client.api_test()

def send_message(channel: str, msg: str):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=msg
        )
    except SlackApiError as e:
        assert e.response["error"]  