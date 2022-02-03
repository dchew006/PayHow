from multiprocessing import context
import constants as keys
from telegram.ext import *
import engine as R

print("Starting engines rrvvv....")

def start_command(update, context):
    update.message.reply_text('type something here to get started')
    
    
def help_command(update, context):
    update.message.reply_text('if you need help google it')
    

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    
    update.message.reply_text(response)

def error(update, context):
    print(f'update {update} caused error {context. error}')
    
def main():
    updater = Updater(keys.API_KEY, use_context = True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_error_handler(error)
    
    updater.start_polling(5)
    updater.idle()
    
main()
    

def print_hi(name):
    
    print(f'Hi, {name}')
    
    if __name__ == '__main__':
        print_hi()