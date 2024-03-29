# Code for local webhook server that accepts bot updates (HTTP POST) from Telegram.
# Expose 'localhost' to the public using a tool such as ngrok.


import os
from dotenv import load_dotenv
from flask import Flask, request
from random import randrange

from quotes import quotes


# Load environment variables from .env
load_dotenv()
SECRET_TOKEN = os.environ.get('SECRET_TOKEN')


# Setup webhook using Flask
app = Flask(__name__)

@app.post('/')
def hello_world():
    if 'x-telegram-bot-api-secret-token' not in request.headers:
        print('Missing secret token')
        return 'OK'; # Acknowledge the update from telegram bot server
    if request.headers['x-telegram-bot-api-secret-token'] != SECRET_TOKEN:
        print('Invalid secret token')
        return 'OK';
    data = request.get_json()
    if 'message' not in data:
        print('Missing message')
        return 'OK';
    message = data['message']
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
    match command:
        case 'start':
            reply_text = 'Welcome to Lol JY Bot'
        case 'slap':
            reply_text = f'JY slaps {from_first_name} around a bit with a large trout'
        case 'leave':
            reply_text = f'{from_first_name} has left the chat'
        case 'lol':
            reply_text = f'Lol {from_first_name}'
        case 'motivate':
            reply_text = quotes[randrange(len(quotes))]
        case _:
            reply_text = 'Unknown bot command'
    return chat_id, reply_text, message_id
