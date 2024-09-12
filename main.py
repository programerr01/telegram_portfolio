import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from helper import generate_json_file, remote_init_and_upload, \
                    upload_to_gh_pages, sanitize_user_name, share_bad_news, \
                    check_for_build_updates
from config import GH_API_TOKEN, GH_USER, GH_TG_TOKEN
import os
import random 

NAME, TITLE, DESCRIPTION, EMAIL, LINKEDIN, IMAGE, THEME = range(7)

THEMES = [
    '🔵',
    '🟣',
    '🟩',
    '🟧',
    '🟦',
    '🟥',   
    '🟨',
    '📗'
]

def start(update, context):
    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        'Hi!\nPlease enter your name:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NAME

def name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('Please enter your title:')
    return TITLE

def title(update, context):
    context.user_data['title'] = update.message.text
    update.message.reply_text('Please enter your Bio:')
    return DESCRIPTION

def description(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text('Please enter your email:')
    return EMAIL

def email(update, context):
    context.user_data['email'] = update.message.text
    update.message.reply_text('Please enter your linkedin:')
    return LINKEDIN

def linkedin(update, context):
    context.user_data['linkedin'] = update.message.text
    update.message.reply_text('Please upload image for your profile:')
    return IMAGE

def image(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('templates/image.jpg')
    
    reply_keyboard = [THEMES]
    update.message.reply_text(
        'Please select a theme:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return THEME

def theme(update, context):
    selected_theme = update.message.text
    context.user_data['theme'] = selected_theme
    update.message.reply_text('Thank you! Your data has been received and you will receive a link shortly.',
                              reply_markup=ReplyKeyboardRemove())

    name = context.user_data['name']
    title = context.user_data['title']
    description = context.user_data['description']
    email = context.user_data['email']
    linkedin = context.user_data['linkedin']
    image_path = 'image.jpg'
    theme = context.user_data['theme']
    user_name = os.environ.get("GH_USER") or GH_USER
    gh_token = os.environ.get("GH_API_TOKEN") or GH_API_TOKEN
    repo_name = name + str(random.randint(1,1000))
    repo_name = sanitize_user_name(repo_name)
    print("Repo name ", repo_name)
    if not repo_name:
        share_bad_news(update)
        return ConversationHandler.END
    
    try:
        generate_json_file(name, title, description, email, linkedin, image_path, theme) 
        remote_init_and_upload(gh_token, user_name, repo_name)
        upload_to_gh_pages(gh_token, user_name, repo_name)
        update.message.reply_text('Portfolio Updated, Please wait for the link to be active.\nWe\'ll notify you once it is live.')

        if check_for_build_updates(gh_token, user_name, repo_name):
            update.message.reply_text(f'Your portfolio is live at: [Portfolio | {name}](https://{user_name}.github.io/{repo_name}/)', parse_mode='Markdown')
    except Exception as e:
        print("Error while in main handler", str(e))
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Conversation cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    BOT_TOKEN = os.environ.get("GH_TG_TOKEN") or GH_TG_TOKEN
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            TITLE: [MessageHandler(Filters.text & ~Filters.command, title)],
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, description)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            LINKEDIN: [MessageHandler(Filters.text & ~Filters.command, linkedin)],
            IMAGE: [MessageHandler(Filters.photo, image)],
            THEME: [MessageHandler(Filters.regex('.*'), theme)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    print("Started....")
    updater.idle()

if __name__ == '__main__':
    main()