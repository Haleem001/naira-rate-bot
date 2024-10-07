
import pytz
import datetime

import json
from telegram.ext import CommandHandler, Updater, Dispatcher
import os
import requests

from dotenv import load_dotenv

load_dotenv()


PORT = int(os.environ.get('PORT', 443))
TOKEN = os.getenv('BOTAPITOKEN')

def create_updater():
    return Updater(token=TOKEN, use_context=True)


url=os.getenv('APIURL')


response = requests.get(
    url)
data = response.text
parse_json = json.loads(data)
rate = parse_json[0]['price']
float_rate = float(rate)
print(rate)


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='/start - Start bot\n' +
        '/help - Show currency list\n' +
        '\n' +
        '/usd - Get current Dollar (USD) rate\n' +
        '/ngnusd - Convert Naira (NGN) to Dollar (USD). Example /ngnusd 1000  \n ' +
        '/usdngn - Convert Dollar (USD) to Naira (NGN). Example /usdngn 100 \n' +
        'For enquiries contact @HaleemG\n'
    )




def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, welcome to dollar to naira rates bot \n "
        'Use /help to show commands list'
    )


# def get_usd(update, context):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text=get_rate_new())
def get_usd2(update, context):
    average_value = float_rate
    nigeria_time = pytz.timezone('Africa/Lagos')
    dt = datetime.datetime.now( nigeria_time)
    dt_string = dt.strftime("%A, %d-%m-%Y  • %H:%M:%S")
    note = '\U0001f4b5'
    cleaned_rate = '{}\n\t\t\t\t\t\t\t USD-NGN \n\t\t\t\t\t\t\t {} 1 USD => ₦{:.2f}'.format(dt_string, note, average_value)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=cleaned_rate )

def ngnusd(update, context):
    real = update.message.text.replace('/ngnusd', '')
    real = real.replace(',', '.')
    real = float(real)
    convert = real/float_rate

    update.message.reply_text('₦{} is ${:.3f}' .format(real, convert))


def usdngn(update, context):

    real = update.message.text.replace('/usdngn', '')
    real = real.replace(',', '.')

    real = float(real)
    convert = real*float_rate

    update.message.reply_text('${} is ₦{:.2f}' .format(real, convert))
updater = create_updater()
dispatcher = updater.dispatcher

def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    updater = create_updater()
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler("usd", get_usd2))
    dispatcher.add_handler(CommandHandler('ngnusd', ngnusd))
    dispatcher.add_handler(CommandHandler('usdngn', usdngn))
    return dispatcher

# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(CommandHandler('help', help))
# dispatcher.add_handler(CommandHandler("usd", get_usd2)) 
# dispatcher.add_handler(CommandHandler('ngnusd' , ngnusd))
# dispatcher.add_handler(CommandHandler('usdngn', usdngn))

# updater.start_polling()
# updater.idle()


# updater.start_webhook(listen="0.0.0.0",
#                           port=int(PORT),
#                           url_path=TOKEN)
# updater.bot.setWebhook('http://localhost:3000' + TOKEN)
