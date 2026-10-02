import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types
import time
import requests

app = Flask(__name__)
@app.route('/')
def home(): return "FX Bot Shop is Live!"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN", "8999675221:AAGETCqP4WH0QjbmolIQRoI06Mq3rThsqhY")
USDT_ADDRESS = "0x307acAdEE363C72C3F388b0AaBE54f81970DC8E"
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY", "YOUR_BSCSCAN_KEY")
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

pending_payments = {}
paid_tx = set()

RISK_DISCLAIMER = (
    "⚠️ RISK DISCLAIMER:\n"
    "Trading Forex, Gold & Crypto involves substantial risk of loss and is not suitable for every investor. "
    "Past performance is not indicative of future results. Our bots are tools to assist trading, not a guarantee of profit. "
    "Trade only with money you can afford to lose. We are not financial advisors."
)

FAKE_ALERT_NOTE = (
    "🔒 ANTI-FAKE ALERT SYSTEM:\n"
    "Our system AUTO-VERIFIES all payments directly on BSC blockchain every 30 seconds. "
    "Fake alerts, edited screenshots, or spoofed transactions will be AUTOMATICALLY REJECTED. "
    "Only confirmed on-chain payments will trigger delivery."
)

def check_payments():
    while True:
        try:
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={USDT_ADDRESS}&startblock=0&endblock=99999999&sort=desc&apikey={BSCSCAN_API_KEY}"
            res = requests.get(url, timeout=20).json()
            if res.get("status") == "1":
                for tx in res.get("result", [])[:20]:
                    tx_hash = tx.get("hash")
                    if tx_hash in paid_tx: continue
                    if tx.get("to","").lower() == USDT_ADDRESS.lower():
                        value = int(tx.get("value",0)) / (10 ** int(tx.get("tokenDecimal",18)))
                        for user_id, order in list(pending_payments.items()):
                            if abs(value - order["price"]) < 0.5:
                                paid_tx.add(tx_hash)
                                b = BOTS[order["bot_id"]]
                                try:
                                    bot.send_message(user_id, f"✅ PAYMENT CONFIRMED ON-CHAIN!\n${value} received\nTX: {tx_hash}\n\nSending your {b['name']}...")
                                    bot.send_message(user_id, f"🎉 Here is your {b['name']}! Thanks for buying.\n\n{RISK_DISCLAIMER}")
                                    bot.send_message(ADMIN_ID, f"✅ AUTO PAID! User {user_id} paid ${value} for {b['name']}\nTX: {tx_hash}")
                                    del pending_payments[user_id]
                                except: pass
        except Exception as e:
            print(e)
        time.sleep(30)

Thread(target=check_payments, daemon=True).start()

@bot.message_handler(commands=['start','shop'])
def start(m):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(f"MA Cross Bot - $199", callback_data="buy_ma_bot"),
        types.InlineKeyboardButton(f"Gold Scalper Pro - $299", callback_data="buy_gold_bot"),
        types.InlineKeyboardButton(f"RSI Market Master - $350", callback_data="buy_rsi_bot")
    )
    welcome = (
        f"FX TRADING MARKET STORE 🚀\n\n"
        f"Welcome {m.from_user.first_name}!\n\n"
        f"{FAKE_ALERT_NOTE}\n\n"
        f"Choose a bot to buy with USDT (BEP20):\n\n"
        f"{RISK_DISCLAIMER}"
    )
    bot.send_message(m.chat.id, welcome, reply_markup=markup)

@bot.message_handler(commands=['terms','risk','disclaimer'])
def terms(m):
    bot.send_message(m.chat.id, f"{FAKE_ALERT_NOTE}\n\n{RISK_DISCLAIMER}")

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        bot.answer_callback_query(call.id)
        uid = call.from_user.id
        if call.data.startswith("buy_"):
            bot_id = call.data.replace("buy_","")
            if bot_id in BOTS:
                b = BOTS[bot_id]
                pending_payments[uid] = {"bot_id": bot_id, "price": b["price"], "time": time.time()}
                text = (
                    f"✅ You selected: {b['name']}\n💰 Price: ${b['price']}\n\n"
                    f"💸 Send EXACT ${b['price']} USDT (BEP20) to:\n`{USDT_ADDRESS}`\n\n"
                    f"{FAKE_ALERT_NOTE}\n\n"
                    f"🤖 Bot will AUTO DETECT payment every 30 seconds. No screenshot needed - fake alert will fail.\n\n"
                    f"{RISK_DISCLAIMER}\n\nYour ID: {uid}"
                )
                bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    except Exception as e:
        print(e)

print("Bot polling...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except:
        time.sleep(5)
