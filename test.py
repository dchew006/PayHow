from telegram.ext import Updater, CommandHandler, callbackcontext
from telegram import Update

def start(update:Update, context:callbackcontext):
    update.message.reply_text("NIHAO {}".format(update.message.from_user.username))



if __name__ == '__main__':
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

