import logging
import os
from dotenv import load_dotenv
from random import randrange
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
TOKEN = os.environ.get('TOKEN')

def verify_token() -> None:
    logging.info('Verifying token...')
    bot = Bot(token=TOKEN)
    try:
        logging.info(f'Verified token | Bot details: {bot.get_me()}')
    except:
        logging.info('Failed to verify token')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Welcome to Lol JY bot')

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

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('slap', slap))
    dispatcher.add_handler(CommandHandler('leave', leave))
    dispatcher.add_handler(CommandHandler('lol', lol))
    dispatcher.add_handler(CommandHandler('motivate', motivate))

    logging.info('Starting bot...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
