import sys
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

try:
    slack_token = os.environ["SLACK_TOKEN"]
    webhook_url = os.environ["WEBHOOK_URL"]
    sw_eng_channel = os.environ["CHANNEL_ID"]
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
    send_message(sw_eng_channel, "Request received")
    return "<p>Slack bot is online</p>"

@app.route('/incoming-webhook', methods=['POST'])
def incoming_webhook():

    try:
        send_message(sw_eng_channel, f"{request.json['Name']} has concluded")
        return Response(response="OK", status=200, mimetype="application/json")
    except SlackApiError as e:
        #print('Error sending message:', e.response['error'])
        return Response(response="NOT OK", status=500, mimetype="application/json")

send_message(sw_eng_channel, "4")
app.run(debug=True, port=3000)

if __name__ == "__main__":
    send_message(sw_eng_channel, "We are gaming")