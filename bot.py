import logging, os
from dotenv import load_dotenv
from random import randrange
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load environment variables from .env
load_dotenv()

# Constants
PORT = 8443
TOKEN = os.environ.get('TOKEN')

# Handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to Lol JY bot', quote=False)

def slap(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    update.message.reply_text(text=f'JY slaps {first_name} around a bit with a large trout', quote=False)

def leave(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    update.message.reply_text(text=f'{first_name} has left the chat', quote=False)

def lol(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    update.message.reply_text(text=f'Lol {first_name}', quote=False)

def motivate(update: Update, context: CallbackContext) -> None:
    with open('quotes.txt', encoding='utf-8') as f:
        quotes = f.readlines()
        quote = quotes[randrange(len(quotes))]
        update.message.reply_text(quote)

# Entry point of application
def main() -> None:
    updater = Updater(token=TOKEN) 

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('slap', slap))
    dispatcher.add_handler(CommandHandler('leave', leave))
    dispatcher.add_handler(CommandHandler('lol', lol))
    dispatcher.add_handler(CommandHandler('motivate', motivate))

    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://lol-jy-bot.herokuapp.com/" + TOKEN
    )
    updater.idle()

if __name__ == '__main__':
    main()
