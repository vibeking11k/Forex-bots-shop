import telebot
from flask import Flask
import threading
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN") # put token for Render Environment
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👋 Welcome to FOREX BOTS SHOP!\n\nWe sell profitable Forex bots.\nType /shop to see available bots.")

# add your other handlers here...

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
