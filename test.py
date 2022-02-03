from telegram.ext import Updater, CommandHandler, callbackcontext
from telegram import Update

from testconfig import TOKEN, PORT


def start(update:Update, context:callbackcontext):
    update.message.reply_text("NIHAO {}".format(update.message.from_user.username))



if __name__ == '__main__':
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_webhook("0.0.0.0", PORT, TOKEN, webhook_url='https://payhowtest.herokuapp.com'+TOKEN)
    updater.idle()

