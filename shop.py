import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types
import time

# --- Keep Render Alive ---
app = Flask(__name__)
@app.route('/')
def home(): return "FX Bot Shop is Live!"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
Thread(target=run_web, daemon=True).start()

# --- Config from Render ---
TOKEN = os.getenv("BOT_TOKEN", "8999675221:AAGETCqP4WH0QjbmolIQRoI06Mq3rThsqhY")
USDT_ADDRESS = "0x307acAdEE363C72C3F388b0AaBE54f81970DC8E"
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "7214398339"))
except:
    ADMIN_ID = 7214398339

bot = telebot.TeleBot(TOKEN, threaded=True)

BOTS = {
    "ma_bot": {"name": "MA Cross Bot", "price": 199},
    "gold_bot": {"name": "Gold Scalper Pro", "price": 299},
    "rsi_bot": {"name": "RSI Market Master", "price": 350}
}

@bot.message_handler(commands=['start', 'shop'])
def start(m):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(f"MA Cross Bot - $199", callback_data="buy_ma_bot"),
        types.InlineKeyboardButton(f"Gold Scalper Pro - $299", callback_data="buy_gold_bot"),
        types.InlineKeyboardButton(f"RSI Market Master - $350", callback_data="buy_rsi_bot")
    )
    bot.send_message(m.chat.id, f"FX TRADING MARKET STORE 🚀\n\nWelcome {m.from_user.first_name}!\nChoose a bot to buy with USDT (BEP20):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        bot.answer_callback_query(call.id)
        uid = call.from_user.id
        if call.data.startswith("buy_"):
            bot_id = call.data.replace("buy_", "")
            if bot_id in BOTS:
                b = BOTS[bot_id]
                text = f"✅ You selected: {b['name']}\n💰 Price: ${b['price']}\n\n💸 Send ${b['price']} USDT (BEP20) to:\n`{USDT_ADDRESS}`\n\nAfter payment, send screenshot or TX hash. Admin will verify and send bot file.\n\nYour ID: {uid}"
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
                bot.send_message(ADMIN_ID, f"🔔 New order!\nUser: {uid} @{call.from_user.username}\nBot: {b['name']} - ${b['price']}")
    except Exception as e:
        print(e)

print("Bot starting polling...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
