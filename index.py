import logging
import os
from dotenv import load_dotenv

from flask import Flask, Blueprint, request, jsonify
from telegram import Bot, Update

from bot import get_dispatcher
load_dotenv()





app = Flask(__name__)
api = Blueprint("serverless_handler", __name__)
bot = Bot(os.environ["BOTAPITOKEN"])
app.config["tg_bot"] = bot
app.config["tg_dispatcher"] = get_dispatcher(bot)
logger = logging.getLogger(__name__)


@api.route("/", methods=["POST"])
def webhook():
    update_json = request.get_json()
    logger.info("input to function %s", update_json)
    update = Update.de_json(update_json, app.config["tg_bot"])
    app.config["tg_dispatcher"].process_update(update)
    return jsonify({"status": "ok"})


@api.route("/")
def home():
    return "Hi there"


app.register_blueprint(api, url_prefix="/api/webhook")