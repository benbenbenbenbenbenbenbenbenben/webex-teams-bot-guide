# Import modules
import json
import requests

# TODO: Get the event (most recent message) that triggered the webhook
def get_message(event, headers):
    url = f'https://api.ciscospark.com/v1/messages/{event["data"]["id"]}'
    response = requests.get(url, headers=headers).json()
    return response['text']

# TODO: Check whether message contains one of multiple possible options
def message_contains(text, options):
    message = text.lower()
    for option in options:
        if option in message:
            return True
    return False

# Post a message in Webex Teams
def post_message(payload, message, headers):
    payload['text'] = message
    requests.post('https://api.ciscospark.com/v1/messages/',headers=headers,json=payload)