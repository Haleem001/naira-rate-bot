
import pytz
from datetime import datetime
import json
from telegram.ext import CommandHandler, Updater, Dispatcher
import os
import requests

from dotenv import load_dotenv

load_dotenv()


PORT = int(os.environ.get('PORT', 443))
TOKEN = os.getenv('BOTAPITOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

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


def get_rate_new():

    # pe
    symbol = parse_json['symbol']
    hr_high = parse_json["highPrice"]
    hr_low = parse_json["lowPrice"]
    float_hr_h = float(hr_high)
    float_hr_low = float(hr_low)
    tz_NG = pytz.timezone('Africa/Lagos')
    now = datetime.now(tz_NG)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    cleaner_rate = "USD-NGN | {}\n\t\t\t\t\t\t\tPRICE: ₦{:.2f}\n\t\t\t\t\t\t\t24hr H: ₦{:.2f}\n\t\t\t\t\t\t\t24hr L: ₦{:.2f}\n".format(
        symbol, float_rate, float_hr_h, float_hr_low) + "\n At {}" .format(dt_string)
    # clean_rate = '$1  is ₦{:.2f} as at {}.'.format(float_rate, dt_string)
    return cleaner_rate


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, welcome to dollar to naira rates bot \n "
        'Use /help to show commands list'
    )


def get_usd(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=get_rate_new())


def ngnusd(update, context):
    # response = requests.get(
    #     'https://api.binance.com/api/v3/ticker/24hr?symbol=USDTNGN')
    # data = response.text
    # parse_json = json.loads(data)
    # rate = parse_json['lastPrice']
    # float_rate = float(rate)
    real = update.message.text.replace('/ngnusd', '')
    real = real.replace(',', '.')

    real = float(real)
    convert = real/float_rate

    update.message.reply_text('₦{} is ${:.3f}' .format(real, convert))


def usdngn(update, context):
    # response = requests.get(
    #     'https://api.binance.com/api/v3/ticker/24hr?symbol=USDTNGN')
    # data = response.text
    # parse_json = json.loads(data)
    # rate = parse_json['lastPrice']
    # float_rate = float(rate)
    real = update.message.text.replace('/usdngn', '')
    real = real.replace(',', '.')

    real = float(real)
    convert = real*float_rate

    update.message.reply_text('${} is ₦{:.2f}' .format(real, convert))


def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler("usd", get_usd))
    dispatcher.add_handler(CommandHandler('ngnusd', ngnusd))
    dispatcher.add_handler(CommandHandler('usdngn', usdngn))
    return dispatcher


# updater.start_polling()
# updater.idle()


# updater.start_webhook(listen="0.0.0.0",
#                           port=int(PORT),
#                           url_path=TOKEN)
# updater.bot.setWebhook('http://localhost:3000' + TOKEN)
