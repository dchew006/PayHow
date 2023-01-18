# import libraries
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import numpy as np
import os

TOKEN = os.environ['API']
PORT = int(os.environ.get('PORT',8443))

################################ HELLO Place Holder #################################
def hello(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(f'Hello {update.effective_user.first_name} this is what the data looks like (debugging purposes)')
  update.message.reply_text(context.user_data)
  
  
  friends = list(context.user_data.keys())
  update.message.reply_text(friends)
  
  paid = []
  for i in list(context.user_data.values()):
     paid.append(float(i[1]))
    
  update.message.reply_text(paid)
  
  numofpeople = len(list(context.user_data.keys()))
  update.message.reply_text(numofpeople)
  
  for i in loanlist:
      update.message.reply_text(i)

################################################################ inline keyboard #################################################################
def start(update: Update, context: CallbackContext) -> None:
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data='HELPMEPLS')],
        [InlineKeyboardButton("Check Entries", callback_data='CHECKENTRIESPLS')],
        [InlineKeyboardButton("Edit Wrong Entry", callback_data='EDITENTRIESPLS')],
        [InlineKeyboardButton("Execute", callback_data='EXECUTEMEPLS')],
        [InlineKeyboardButton("Reset", callback_data='RESETMEPLS')],
        # [InlineKeyboardButton("Show Working", callback_data='SHOWWORKINGPLS')],
        # [InlineKeyboardButton("PayLah", callback_data='PAYLAHMEPLS')],
        ]
    )
    update.message.reply_text(
        f'Hello {update.effective_user.first_name} and friends\nWelcome to PayHow, your personal bill splitter.\n\nTo get started, return what you and your friends paid in the following format: X paid Y\nFor example: Sarah paid 45.60\n\nOnce the entries have been recorded, choose one of the options below:',
        reply_markup=reply_buttons
    )
################################################################ LOGIC #################################################################
################################################################ Respond to button #################################################################
def button(update: Update, context: CallbackContext) -> None:
    # Must call answer!
    update.callback_query.answer()


    ############### RESET BUTTON RESPONSE ################
    RESETMEPLS = update.callback_query.data
    if RESETMEPLS == "RESETMEPLS":
        context.user_data.clear()
        loanlist.clear()
        update.callback_query.message.edit_text("All records have been successfully wiped!")
        
        
    ############ HELP MENU RESPONSE ################
    HELPMEPLS = update.callback_query.data
    if HELPMEPLS == 'HELPMEPLS':
        update.callback_query.message.reply_text(f'Hello {update.effective_user.first_name} and friends,\nWelcome to PayHow! the bot that splits your bills evenly with the least transactions possible\n\nPlease return what you and your friends paid in the following format: X paid Y \nFor example: Sarah paid 45\n\nNote: Use a Single Name, Include friends who paid 0 too, Dont add symbols like $ for amounts\n\nTo run the bot, type /execute\nTo check your list of entries, type /show\nTo reset your entries, type /reset\n')
    
    
    ################ CHECK ENTRIES RESPONSE ################
    CHECKENTRIESPLS = update.callback_query.data
    if CHECKENTRIESPLS == "CHECKENTRIESPLS":
        reply_list = [f'Hi {update.effective_user.first_name},']
        if context.user_data:
            reply_list.append('here\'s the list of transactions you\'ve entered so far:\n')
            reply_list.extend([f'{key} {value_pair[0]} {value_pair[1]}' for (key, value_pair) in context.user_data.items()])
        else:
            reply_list.append('No entries so far :(')
        reply_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Execute", callback_data='EXECUTEMEPLS')],
            [InlineKeyboardButton("Edit Entry", callback_data='EDITENTRIESPLS')],
            [InlineKeyboardButton("Reset", callback_data='RESETMEPLS')],
            ]
        )
        update.callback_query.message.reply_text('\n'.join(reply_list), reply_markup=reply_buttons)
        
    
    ################################ EDIT ENTRY RESPONSE ################################
    EDITENTRIESPLS = update.callback_query.data
    if EDITENTRIESPLS == 'EDITENTRIESPLS':
        reply_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Execute", callback_data='EXECUTEMEPLS')],
            [InlineKeyboardButton("Edit Entry", callback_data='EDITENTRIESPLS')],
            [InlineKeyboardButton("Reset", callback_data='RESETMEPLS')],
            ]
        )
        update.callback_query.message.reply_text(f'Ayio {update.effective_user.first_name} press wrong how?\nIts ok. To edit a wrong entry just retype the same name with the corrected amount.\n\nFor example:\nOld input: Sam paid 10 (wrong amount)\nNew Input: Sam paid 50(correct amount)\n\nTo check your entries again, type /show to see the full entry list.',reply_markup=reply_buttons)
        
        
    # ################################ PAYLAH RESPONSE #################################
    # PAYLAHMEPLS = update.callback_query.data
    # if PAYLAHMEPLS == "PAYLAHMEPLS":
    #     update.callback_query.message.edit_text(f'@PayLahBot 20')
    #     update.callback_query.message.reply_text('@PayLahBot 34')
    #     update.callback_query.message.reply_text('@PayLahBot 54')

    ################ EXECUTE RESPONSE #################
    EXECUTEMEPLS = update.callback_query.data
    if EXECUTEMEPLS == "EXECUTEMEPLS":
        for i in loanlist:
            ################################ AD HOC LOANS #################################
            if str(i['lender']) in [key for (key, value) in context.user_data.items()]:
                lender_old_bal = float([value for (key, value) in context.user_data.items() if key == str(i['lender'])][0][1])
                lender_adj_bal = lender_old_bal + float(i['amount'])
                context.user_data[str(i['lender'])] = ('paid', str(lender_adj_bal))
            else:
                lender_fresh = float(i['amount'])
                context.user_data[str(i['lender'])] = ('paid', str(lender_fresh))

            if str(i['lendee']) in [key for (key, value) in context.user_data.items()]:
                lendee_old_bal = float([value for (key, value) in context.user_data.items() if key == str(i['lendee'])][0][1])
                lendee_adj_bal = lendee_old_bal - float(i['amount'])
                context.user_data[str(i['lendee'])] = ('paid', str(lendee_adj_bal))
            else:
                lendee_fresh = float(i['amount'])*-1
                context.user_data[str(i['lendee'])] = ('paid', str(lendee_fresh))
        
        update.callback_query.message.reply_text('Eh hello time to pay your dues! Payment structure is as follows:')

        #friend and paid list
        friends = list(context.user_data.keys())
        paid = []
        for i in list(context.user_data.values()):
            paid.append(float(i[1]))
        
        #transforming data for df
        numofpeople = len(friends)
        spent = np.array(paid).reshape(-1,1)
        per_person = spent/ len(paid)
        table = (per_person.T - per_person).clip(min=0).round(2)

        #plugging data for algo
        n = numofpeople
        myarray = table

        ################################
        #least cash flow algorithm
        ################################
                    
        #return index of min values
        def getmin(arg):
            
            minInd = 0
            for i in range(1, n):
                if (arg[i] < arg[minInd]):
                    minInd = i
            return minInd
        
        # index of max values
        def getmax(arg):
    
            maxInd = 0
            for i in range(1, n):
                if (arg[i] > arg[maxInd]):
                    maxInd = i
            return maxInd

        #return min of the two values
        def minof2(x,y):
            if x < y:
                return x
            else:
                return y
            
        def mincashflowrec(amount):
            #Maxcr is the max to be cr to another person
            #maxDr is the max to be taken from another person
            maxCr = getmax(amount)
            MaxDr = getmin(amount)
            
            #if balance, amounts settled.
            if (amount[maxCr] < 0.00001 and amount[MaxDr] < 0.00001):
                return 0
            
            #min of a indiv's net balance
            min = minof2(-amount[MaxDr], amount[maxCr])
            amount[maxCr] = amount[maxCr] - min
            amount[MaxDr] = amount[MaxDr] + min
            
            Payer = friends[MaxDr]
            Payee = friends[maxCr]
            
            update.callback_query.message.reply_text(str(Payer) + " pays $" + str(min.round(2)) + " to " + str(Payee))
            # print(Payer, "pays ", min.round(2), " to ", Payee)
            
            #repeats within array until either maxdr or maxcr becomes 0
            
            mincashflowrec(amount)

        #input[a][b] where a needs to pay b
        def cashflow(input):
            amount = [0 for i in range(n)]
            #initialise all 0
            #create array

            for i in range(n):
                for j in range(n):
                    amount[i] += (input[j][i] - input[i][j])
            
            mincashflowrec(amount)

        input = myarray
        cashflow(input)
        
        loanlist.clear()
        context.user_data.clear()

################################################################ Help Menu #################################################################
def helper(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.effective_user.first_name} and friends!\nWelcome to PayHow, the bot that splits your bills evenly.\n\nPlease return what you and your friends paid in the following format: X paid Y \nFor example: Sarah paid 45\n\nNote:\nUse a single word names,\nInclude friends who paid $0 too,\nDont add symbols like $ for amounts\n\nTo run the bot, type /execute\nTo check your entries, type /check\nTo reset your entries, type /reset')

################################ Show Transactions #################################
def showme(update: Update, context: CallbackContext) -> int:
    reply_list = [f'Hi {update.effective_user.first_name},']
    reply_list.append('here\'s the list of transactions you\'ve entered so far:\n')
    
    for i in loanlist:
        lender = str(i['lender'])
        lendee = str(i['lendee'])
        loanvalue = str(i['amount'])
        reply_list.append(f'{lendee} owes {lender} ${loanvalue}')
        
    if context.user_data:
        reply_list.extend([f'{key} {value_pair[0]} ${value_pair[1]}' for (key, value_pair) in context.user_data.items()])
    elif len(loanlist) > 0:
        reply_list.append('')
    else:
        reply_list.append('No entries so far :(')
    
   
    ################################ Embedded inlinekeyboard options to either reset or confirm execution #################################
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Execute", callback_data='EXECUTEMEPLS')],
        [InlineKeyboardButton("Reset", callback_data='RESETMEPLS')],
        ]
    )
  
    update.message.reply_text('\n'.join(reply_list), reply_markup=reply_buttons)



############################################################################ ledger updater #################################################################
def personal(update: Update, context: CallbackContext) -> int:
    reply_list = [f'Lets get started {update.effective_user.first_name}!\n']
    if context.user_data:
        reply_list.append('Heres the transactions you\'ve entered so far:\n')
        reply_list.extend([f'{key} {value_pair[0]} {value_pair[1]}' for (key, value_pair) in context.user_data.items()])
        # if user input does not match X paid Y format, print an error message
        if not context.args:
            reply_list.append('\nPlease enter your transactions in the following format: X paid Y\nFor example: Sarah paid 45\n')
    else:
        reply_list.append('No entries so far ..')
    reply_list.extend([
        '\nTo get started, indicate the amount you and your friends paid using the format below',
        'Use the format: X paid Y',
        'For example: Sally paid 45.60',
        '\n To view your list of successful entires, type /show'
    ])
    update.message.reply_text('\n'.join(reply_list))
    
################################################################ regex reader to parse data #################################################################
INFO_REGEX = r'^([\w\-]+) (paid) (.+)$'
def receive_info(update: Update, context: CallbackContext) -> int:
    # Extract the three capture groups
    info = re.match(INFO_REGEX, update.message.text).groups()
    # Using the first capture group as key, the second and third capture group are saved as a pair to the context.user_data
    context.user_data[info[0]] = (info[1], info[2])

    # Quote the information in the reply
    update.message.reply_text(
        f'Gotcha! {info[0]} {info[1]} {info[2]}. Input successful.'
    )
    
    #info0 = name
    #info1 = 'paid'
    #info2 = amount

################################################################ regex reader to parse data #################################################################
LOAN_REGEX = r'^([\w\-]+) (loaned) (.+) (.+)$'
loanlist = []


def receive_info_loan(update: Update, context: CallbackContext) -> int:
    info_loan = re.match(LOAN_REGEX, update.message.text).groups()
    data = {
        'lender': info_loan[0],
        'lendee': info_loan[2],
        'amount': info_loan[3]
    }

    loanlist.append(data)

    update.message.reply_text(
        f'{info_loan[0]} lent {info_loan[2]} ${info_loan[3]}.'
    )

# info0 = lender
# info1 = 'loaned'
# info2 = borrower
# info3 = amount

################################################################ Reset button #########################################################################
def resetvalues(update: Update, context: CallbackContext):
    context.user_data.clear()
    loanlist.clear()
    update.message.reply_text("All records have been successfully wiped!")
    
    
################################################################ Execute button #########################################################################
def executemepls(update: Update, context: CallbackContext):
    for i in loanlist:
        ######################### AD HOC LOANS ##############################
        if str(i['lender']) in [key for (key, value) in context.user_data.items()]:
            lender_old_bal = float([value for (key, value) in context.user_data.items() if key == str(i['lender'])][0][1])
            lender_adj_bal = lender_old_bal + float(i['amount'])
            context.user_data[str(i['lender'])] = ('paid', str(lender_adj_bal))
        else:
            lender_fresh = float(i['amount'])
            context.user_data[str(i['lender'])] = ('paid', str(lender_fresh))

        if str(i['lendee']) in [key for (key, value) in context.user_data.items()]:
            lendee_old_bal = float([value for (key, value) in context.user_data.items() if key == str(i['lendee'])][0][1])
            lendee_adj_bal = lendee_old_bal - float(i['amount'])
            context.user_data[str(i['lendee'])] = ('paid', str(lendee_adj_bal))
        else:
            lendee_fresh = float(i['amount'])*-1
            context.user_data[str(i['lendee'])] = ('paid', str(lendee_fresh))
    
    update.message.reply_text('Time to pay your dues! Payment structure is as follows:')

    #friend and paid list
    friends = list(context.user_data.keys())
    paid = []
    for i in list(context.user_data.values()):
        paid.append(float(i[1]))
        
    #transforming data for df
    numofpeople = len(friends)
    spent = np.array(paid).reshape(-1,1)
    per_person = spent/ len(paid)
    table = (per_person.T - per_person).clip(min=0).round(2)

    #plugging data for algo
    n = numofpeople
    myarray = table

    ################################
    #least cash flow algorithm
    ################################                    

    def getmin(arg):            
        minInd = 0
        for i in range(1, n):
            if (arg[i] < arg[minInd]):
                minInd = i
        return minInd
        
    # index of max values
    def getmax(arg):
        maxInd = 0
        for i in range(1, n):
            if (arg[i] > arg[maxInd]):
                maxInd = i
        return maxInd

    #return min of the two values
    def minof2(x,y):
        if x < y:
            return x
        else:
            return y            
    def mincashflowrec(amount):
        #Maxcr is the max to be cr to another person
        #maxDr is the max to be taken from another person
        maxCr = getmax(amount)
        MaxDr = getmin(amount)            
        #if balance, amounts settled.
        if (amount[maxCr] < 0.00001 and amount[MaxDr] < 0.00001):
            return 0            
        #min of a indiv's net balance
        min = minof2(-amount[MaxDr], amount[maxCr])
        amount[maxCr] = amount[maxCr] - min
        amount[MaxDr] = amount[MaxDr] + min            
        Payer = friends[MaxDr]
        Payee = friends[maxCr]            
        update.message.reply_text(str(Payer) + " pays $" + str(min.round(2)) + " to " + str(Payee))
        
        mincashflowrec(amount)

    #input[a][b] where a needs to pay b
    def cashflow(input):
        amount = [0 for i in range(n)]
        #initialise all 0
        #create array

        for i in range(n):
            for j in range(n):
                amount[i] += (input[j][i] - input[i][j])            
        mincashflowrec(amount)

    input = myarray
    cashflow(input)
    
    loanlist.clear()
    context.user_data.clear()

######################################################################## wrong entry how button #################################################################
def presswrong(update: Update, context: CallbackContext):

    update.message.reply_text(f'Ayio {update.effective_user.first_name} press wrong how?\nIts ok. To edit a wrong entry just retype the same name with the corrected amount.\n\nFor example:\nOld input: Sam paid 10 (wrong amount)\nNew Input: Sam paid 50(correct amount)\n\nTo check your entries again, type /show to see the full entry list.')

################################################################ Handlers Below #################################################################
def main():
    #TOKEN
    updater = Updater(TOKEN, use_context=True)

    #Handlers
    updater.dispatcher.add_handler(CommandHandler('reset', resetvalues))
    updater.dispatcher.add_handler(CommandHandler('edit', presswrong))
    updater.dispatcher.add_handler(CommandHandler('show', showme))
    updater.dispatcher.add_handler(CommandHandler('Execute', executemepls))
    updater.dispatcher.add_handler(CommandHandler('help', helper))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(INFO_REGEX), receive_info))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(LOAN_REGEX), receive_info_loan))

    #Connect to Telegram and start polling
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://payhow.herokuapp.com/'+TOKEN)

    #Keep running until interrupted
    updater.idle()

if __name__ == '__main__':
    main()