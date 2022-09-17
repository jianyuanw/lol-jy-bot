# Code for AWS Lambda function that acts as a webhook for Telegram bot updates.
# Does not work on its own (ie. "python bot_lambda.py" will fail).
# Only requires Python's standard libraries.


import json
import os
from random import randrange

from quotes import quotes


# Load environment variables
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')


# AWS Lambda handler function
def lambda_handler(event, context):
    if 'x-telegram-bot-api-secret-token' not in event['headers']:
        print('Missing secret token')
        return 'OK'; # Acknowledge the update from telegram bot server
    if event['headers']['x-telegram-bot-api-secret-token'] != SECRET_TOKEN:
        print('Invalid secret token')
        return 'OK';
    body = json.loads(event['body'])
    if 'message' not in body:
        print('Missing message')
        return 'OK';
    message = body['message']
    if 'entities' not in message:
        print('Missing entities')
        return 'OK';
    entities = message['entities']
    if entities[0]['type'] != 'bot_command':
        print('Not a bot command')
        return 'OK';
    chat_id, text, reply_to_message_id = process_bot_command(message)
    return {
        'method': 'sendMessage',
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': reply_to_message_id
    }


# Handlers
def process_bot_command(message) -> tuple[int, str, int]:
    message_id = message['message_id']
    from_first_name = message['from']['first_name']
    chat_id = message['chat']['id']
    text = message['text']
    index_at = text.find('@')
    if index_at != -1:
        text = text[:index_at]
    command = text[1:].strip()
    # Changed match-case to if-loop as AWS Lambda uses Python 3.9 which does not
    # yet support match-case.
    if command == 'start':
        reply_text = 'Welcome to Lol JY Bot'
    elif command == 'slap':
        reply_text = f'JY slaps {from_first_name} around a bit with a large trout'
    elif command == 'leave':
        reply_text = f'{from_first_name} has left the chat'
    elif command == 'lol':
        reply_text = f'Lol {from_first_name}'
    elif command == 'motivate':
        reply_text = quotes[randrange(len(quotes))]
    else:
        reply_text = 'Unknown bot command'
    return chat_id, reply_text, message_id
