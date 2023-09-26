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
    try:
        response = client.files_upload(
            channels=channel,
            file="./synnax.png",
            initial_comment="Here's an image:",
        )
    except SlackApiError as e:
        assert e.response["error"]

def send_image_from_link(channel: str, image_url: str):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text="Here's an image:",
            blocks=[
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Image",
                }
            ],
        )
    except SlackApiError as e:
        assert e.response["error"]


@app.route("/")
def is_online():
    return "<p>Slack bot is online</p>"

@app.route('/incoming-webhook', methods=['POST'])
def incoming_webhook():

    try:
        send_message(sw_eng_channel, f"{request.json['Name']} has concluded")
        return Response(response="OK", status=200, mimetype="application/json")
    except SlackApiError as e:
        #print('Error sending message:', e.response['error'])
        return Response(response="NOT OK", status=500, mimetype="application/json")

@app.route("/send_file", methods=['POST'])
def send_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    try:
        file.save("f.png")
        response = client.files_upload(
            channels=sw_eng_channel,
            file='./f.png',
            initial_comment="Here's an image:",
        )
        os.remove("f.png")
        return Response(response="OK", status=200)
    except SlackApiError as e:
        assert e.response["error"]
        return Response(response="NOT OK", status=500)

@app.route("/webhook", methods=['POST'])
def receive_test():
    if 'file' in request.files:
            try:
                file = request.files['file']
                file.save("f.png")
                response = client.files_upload(
                    channels=sw_eng_channel,
                    file='./f.png',
                    initial_comment=f"{request.json['Name']} has concluded",
                )
                os.remove("f.png")
                return Response(response="OK", status=200, mimetype="application/json")
            except SlackApiError as e:
                assert e.response["error"]
                return Response(response="NOT OK", status=500, mimetype="application/json")
    else:
        try:
            send_message(sw_eng_channel, f"{request.json['Name']} has concluded")
            return Response(response="OK", status=200, mimetype="application/json")
        except SlackApiError as e:
            #print('Error sending message:', e.response['error'])
            return Response(response="NOT OK", status=500, mimetype="application/json")

if __name__ == "__main__":
    #send_message(sw_eng_channel, "We are gaming")
    #send_graph(sw_eng_channel)
    app.run(host='0.0.0.0', debug=True, port=3000)