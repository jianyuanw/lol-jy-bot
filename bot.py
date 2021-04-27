import os, logging
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
TOKEN = os.environ.get('TOKEN')

def verify_token() -> None:
    logging.info('Verifying token')
    bot = Bot(token=TOKEN)
    try:
        logging.info(f'Verified token | Bot details: {bot.get_me()}')
    except:
        logging.info('Failed to verify token')

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    # dispatcher = updater.dispatcher

    # dispatcher.add_handler(CommandHandler('start', start))

    # updater.start_polling()
    # updater.idle()

if __name__ == '__main__':
    main()
