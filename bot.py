import datetime
import logging
import os
import pytz
import requests
from dotenv import load_dotenv
from random import randrange
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram.ext.jobqueue import Days

# logging.basicConfig(filename='bot.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
TOKEN = os.environ.get('TOKEN')
TEST_CHAT_ID = '-568078567'
FUNNY_CHAT_ID = '-1001417249364'

def verify_token() -> None:
    logging.info('Verifying token...')
    bot = Bot(token=TOKEN)
    try:
        logging.info(f'Verified token | Bot details: {bot.get_me()}')
    except:
        logging.info('Failed to verify token')

def start(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    # logging.info(f'Received command /start from {first_name}')
    update.message.reply_text(f'Welcome to Lol JY bot')

def slap(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received command /slap from {first_name} in {group_title}')
    update.message.reply_text(text=f'JY slaps {first_name} around a bit with a large trout', quote=False)

def leave(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received command /leave from {first_name} in {group_title}')
    update.message.reply_text(text=f'{first_name} has left the chat', quote=False)

def lol(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received command /lol from {first_name} in {group_title}')
    update.message.reply_text(text=f'Lol {first_name}', quote=False)

def motivate(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received command /motivate from {first_name} in {group_title}')
    result = requests.get('https://type.fit/api/quotes').json()
    quote = result[randrange(len(result))]
    text = quote['text']
    author = quote['author']
    message = f'"{text}"\n- {author}'
    update.message.reply_text(message)

def countdownto(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) == 0:
        update.message.reply_text('Hi! Use "/countdownto DDMMM" to perform the countdown.')
    else:
        date_str = args[0]
        try:
            date_today = datetime.date.today()
            date_str += str(date_today.year)
            date_countdownto = datetime.datetime.strptime(date_str, '%d%b%Y').date()
            days = (date_countdownto - date_today).days
            update.message.reply_text(f'{days} more day(s) to freedom!')
        except ValueError:
            update.message.reply_text('Incorrect date format. Please enter in DDMMM format (eg. 01Jan).')

def sticker(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received sticker from {first_name} in {group_title}')
    update.message.reply_text(f'Lol {first_name}, please engage in meaningful conversation.')

def gif(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    # logging.info(f'Received GIF from {first_name} in {group_title}')
    update.message.reply_text(f'Lol {first_name}, please engage in meaningful conversation.')

def edited_message(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    message_id = update.edited_message.message_id
    original_message = context.chat_data.get(message_id, 'Not found')
    # logging.info(f'Detected edited message by {first_name} in {group_title}. Original message: "{original_message}"')
    update.edited_message.reply_text(f'Caught tampering with evidence!\nOriginal message: "{original_message}"')

def all_messages(update: Update, context: CallbackContext) -> None:
    message_id = update.message.message_id
    message = update.message.text
    # logging.info(f'Storing message | Message ID: {message_id} | Message: {message}')
    context.chat_data[message_id] = message
    if 'hang' in message.lower():
        update.message.reply_text('Remember to include time/place/activity')

def test(update: Update, context: CallbackContext) -> None:
    date_countdownto = datetime.date(2021, 6, 24)
    date_today = datetime.date.today()
    days = (date_countdownto - date_today).days
    context.bot.send_message(chat_id=FUNNY_CHAT_ID, text=f'{days} more day(s) to freedom!')

def countdown_daily(context: CallbackContext) -> None:
    date_countdownto = datetime.date(2021, 6, 24)
    date_today = datetime.date.today()
    days = (date_countdownto - date_today).days
    context.bot.send_message(chat_id=FUNNY_CHAT_ID, text=f'Good morning. {days} more day(s) to freedom!')

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('slap', slap))
    dispatcher.add_handler(CommandHandler('leave', leave))
    dispatcher.add_handler(CommandHandler('lol', lol))
    dispatcher.add_handler(CommandHandler('motivate', motivate))
    dispatcher.add_handler(CommandHandler('countdownto', countdownto))
    # dispatcher.add_handler(MessageHandler(Filters.sticker, sticker))
    # dispatcher.add_handler(MessageHandler(Filters.document.gif, gif))
    # dispatcher.add_handler(MessageHandler(Filters.update.edited_message, edited_message))
    # dispatcher.add_handler(MessageHandler(Filters.text, all_messages))
    dispatcher.add_handler(CommandHandler('test', test))

    job_queue = updater.job_queue
    timezone = pytz.timezone('Asia/Singapore')
    time = datetime.time(hour=7, tzinfo=timezone)
    job_queue.run_daily(countdown_daily, time)

    logging.info('Starting bot...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
