# Import modules
from flask import request
from chatbot import *

# Variables
bot_token = "token"
bot_email = "yourbot@webex.bot"

# Main handler function
def handler(request):
    webhook_event = request.get_json()
    print(webhook_event)

    headers = {
        'authorization': f'Bearer {bot_token}' 
    }
    payload = {'roomId': webhook_event['data']['roomId']}

    # Ignore Bots Messages
    if webhook_event['resource'] == 'messages' and webhook_event['data']['personEmail'] == bot_email:
        return 'success'

    # Get Message Text From Webhook Alert
    if webhook_event['resource'] == 'messages':
        message = get_message(webhook_event, headers)
        print('Text Received: ' + message)

      # Respond To Users Messages
    if message_contains(message, ['hello', 'hi', 'greetings', 'gday']):
        post_message(payload,'Hello Human', headers)

    return 'success'