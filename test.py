import telebot
from telegram.ext import Updater, commandhandler, messagehandler, filters
import os

TOKEN = telebot.TeleBot("5038866075:AAEIhqiNHq6HTq_3KWgGq8cRe1XacK9mPmk")

def start(update, context):
    yourname = update.message.chat.first_name
    msg ="Hi" + yourname+"! Welcome to the mimic bot!"
    context.bot.send_message(update.message.chat.id, msg)

def mimic(update, context):
    context.bot.send_message(update.bot.message.chat.id, update.message.text)

def details(update, context):
    context.bot.send_message(update.message.chat.id, update.message)

def error(update, context):
    context.bot.send_message(update.message.chat.id, "Oops error encountered!")

def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    dp.add_handler(commandhandler("/start", start))
    dp.add_handler(messagehandler(filter.text, mimic))
    dp.add_handler(commandhandler("/details", details))
    dp.add_handler(error)

    #WEBHOOK
    updater.start_webhook(listen="0.0.0.0", port=os.environ.get("PORT", 443),
                          url_path=TOKEN,
                          webhook_url="https://payhowtest.herokuapp.com"+TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()