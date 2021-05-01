import os, logging
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

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
    first_name = update.effective_user.first_name
    logging.info(f'Received command /start from {first_name}')
    update.message.reply_text(f'Lol {first_name}')

def sticker(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received sticker from {first_name} in {group_title}')
    update.message.reply_text(f'Hi {first_name}, please engage in meaningful conversation.')

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.sticker, sticker))

    logging.info('Starting bot...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# Ideas:
# Catch message edits