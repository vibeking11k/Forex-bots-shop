import telebot
from telebot import types
import time, json, traceback
from datetime import datetime

TOKEN = "8999675221:AAGETCqP4WH0OjbmolIQRolO6Mq3rThsqhY"
USDT_ADDRESS = "0x307acAdEE363C72C3F388b0aAbE54fF81970DC81"
ADMIN_ID = 0

bot = telebot.TeleBot(TOKEN, threaded=True)

BOTS = {
    "ma_bot": {"name": "MA Cross Bot", "price": 29},
    "gold_bot": {"name": "Gold Scalper Pro", "price": 49},
    "rsi_bot": {"name": "RSI Market Master", "price": 39}
}

@bot.message_handler(commands=['start'])
def start(m):
    global ADMIN_ID
    if ADMIN_ID == 0:
        ADMIN_ID = m.chat.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("MA Cross Bot - $29", callback_data="buy_ma_bot"),
        types.InlineKeyboardButton("Gold Scalper Pro - $49", callback_data="buy_gold_bot"),
        types.InlineKeyboardButton("RSI Master Bot - $39", callback_data="buy_rsi_bot")
    )
    bot.send_message(m.chat.id, f"FX TRADING MARKET STORE\n\nChoose bot to buy:\nInstant delivery after USDT payment", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        bot.answer_callback_query(call.id)
        uid = call.from_user.id
        if call.data.startswith("buy_"):
            bot_id = call.data.replace("buy_", "")
            b = BOTS[bot_id]
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f"I Have Paid ${b['price']}", callback_data=f"paid_{bot_id}"))
            bot.send_message(uid, f"*{b['name']} - ${b['price']}*\n\nPAY HERE:\n`{USDT_ADDRESS}`\n\nUse BEP20 only!", parse_mode="Markdown", reply_markup=markup)
        elif call.data.startswith("paid_"):
            bot.send_message(uid, "Send your payment screenshot now! Admin will verify in 5 mins.")
            if ADMIN_ID != 0:
                try: bot.send_message(ADMIN_ID, f"NEW PAYMENT from {uid}")
                except: pass
    except Exception as e:
        print(e)

print("STORE STARTING... 24/7 ACTIVE")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, none_stop=True)
    except:
        time.sleep(5)