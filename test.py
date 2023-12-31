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
    print("send graph")
    try:
        response = client.files_upload(
            channels=channel,
            file="./synnax.png",
            initial_comment="Here's an image:",
        )
    except SlackApiError as e:
        assert e.response["error"]


if __name__ == "__main__":
    send_graph(sw_eng_channel)