import sys
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

try:
    slack_token = os.environ["SLACK_TOKEN"]
    webhook_url = os.environ["WEBHOOK_URL"]
    sw_eng_channel = os.environ["SOFTWARE_ENGINEERING_CHANNEL"]
except:
    logging.warning("Missing environmental variables")
    print("Missing environmental variables")

client = WebClient(token=slack_token)
webhook = WebhookClient(webhook_url)
api_response = client.api_test()

def send_message(channel: str, msg: str):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=msg
        )
    except SlackApiError as e:
        assert e.response["error"]  

def send_graph(channel: str):
    pass

@app.route("/")
def is_online():
    return "<p>Slack bot is online</p>"

# Unsure abt this part
# If there is another method to get webhooks, I'll do it
# Will test once I get webhook url
@app.route('/incoming-webhook', methods=['POST'])
def incoming_webhook():
    data = request.json
    text = data.get('text', '')

    try:
        response = client.chat_postMessage(
            # Will either extract channel from webhook, or do some logic
            channel='',
            # placehold text for now
            text=""
        )
        print('Message sent:', response)
        return jsonify({'message': 'Message sent to Slack'}), 200
    except SlackApiError as e:
        print('Error sending message:', e.response['error'])
        return jsonify({'error': 'Error sending message to Slack'}), 500

app.run(debug=True, port=3000)

if __name__ == "__main__":
    send_message(sw_eng_channel, "We are gaming")