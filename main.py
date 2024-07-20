import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from helper import generate_json_file,remote_init_and_upload,upload_to_gh_pages
from config import GH_TOKEN, GH_USER,  GH_TG_TOKEN
import os
import random 

NAME, TITLE, DESCRIPTION, EMAIL, IMAGE = range(5)

# Start command handler
def start(update, context):
    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Hi!\nPlease enter your name:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NAME

# Name handler
def name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('Please enter your title:')
    return TITLE

# Title handler
def title(update, context):
    context.user_data['title'] = update.message.text
    update.message.reply_text('Please enter the description:')
    return DESCRIPTION

# Description handler
def description(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text('Please enter your email:')
    return EMAIL

# Email handler
def email(update, context):
    context.user_data['email'] = update.message.text
    update.message.reply_text('Please send an image:')
    return IMAGE

# Image handler
def image(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('templates/image.jpg')
    update.message.reply_text('Thank you! Your data has been received and you will recieve link shortly.')
    #send another message to the user

    # Process the received data here
    name = context.user_data['name']
    title = context.user_data['title']
    description = context.user_data['description']
    email = context.user_data['email']
    image_path = 'image.jpg'

    user_name = os.environ.get("GH_USER") or GH_USER
    gh_token = os.environ.get("GH_API_TOKEN") or GH_TOKEN
    repo_name = name.replace(" ", "_") + str(random.randint(1,1000))
    generate_json_file(name, title, description, email, image_path);
    remote_init_and_upload(gh_token,user_name,repo_name)
    upload_to_gh_pages(gh_token,user_name,repo_name)
    update.message.reply_text(f'https://{user_name}.github.io/{repo_name}/')
    update.message.reply_text(f'It might take upto 2 minutes for the link to be active. Please be patient.')

    return ConversationHandler.END

# Cancel command handler
def cancel(update, context):
    update.message.reply_text('Conversation cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token
    BOT_TOKEN = os.environ.get("GH_TG_TOKEN") or GH_TG_TOKEN
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Create the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            TITLE: [MessageHandler(Filters.text, title)],
            DESCRIPTION: [MessageHandler(Filters.text, description)],
            EMAIL: [MessageHandler(Filters.text, email)],
            IMAGE: [MessageHandler(Filters.photo, image)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()