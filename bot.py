import os, logging
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

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
    update.message.reply_text(f'Welcome to Lol JY bot')

def slap(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received command /slap from {first_name} in {group_title}')
    update.message.reply_text(text=f'JY slaps {first_name} around a bit with a large trout', quote=False)

def leave(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received command /leave from {first_name} in {group_title}')
    update.message.reply_text(text=f'{first_name} has left the chat', quote=False)

def lol(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received command /lol from {first_name} in {group_title}')
    update.message.reply_text(text=f'Lol {first_name}', quote=False)

def sticker(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received sticker from {first_name} in {group_title}')
    update.message.reply_text(f'Lol {first_name}, please engage in meaningful conversation.')

def gif(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    logging.info(f'Received GIF from {first_name} in {group_title}')
    update.message.reply_text(f'Lol {first_name}, please engage in meaningful conversation.')

def edited_message(update: Update, context: CallbackContext) -> None:
    first_name = update.effective_user.first_name
    group_title = update.effective_chat.title
    message_id = update.edited_message.message_id
    original_message = context.chat_data.get(message_id, 'Not found')
    logging.info(f'Detected edited message by {first_name} in {group_title}. Original message: "{original_message}"')
    update.edited_message.reply_text(f'Caught tampering with evidence!\nOriginal message: "{original_message}"')

def all_messages(update: Update, context: CallbackContext) -> None:
    message_id = update.message.message_id
    message = update.message.text
    logging.info(f'Storing message | Message ID: {message_id} | Message: {message}')
    context.chat_data[message_id] = message
    if 'hang' in message.lower():
        update.message.reply_text('Remember to include time/place/activity')

def main() -> None:
    verify_token()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('slap', slap))
    dispatcher.add_handler(CommandHandler('leave', leave))
    dispatcher.add_handler(CommandHandler('lol', lol))
    dispatcher.add_handler(MessageHandler(Filters.sticker, sticker))
    dispatcher.add_handler(MessageHandler(Filters.document.gif, gif))
    dispatcher.add_handler(MessageHandler(Filters.update.edited_message, edited_message))
    dispatcher.add_handler(MessageHandler(Filters.text, all_messages))

    logging.info('Starting bot...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
