import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types
import time
import requests

app = Flask(__name__)
@app.route('/')
def home(): return "FOREX BOTS SHOP is Live!"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN", "8999675221:AAGETCqP4WH0QjbmolIQRoI06Mq3rThsqhY")
USDT_ADDRESS = "0x307acAdEE363C72C3F388b0AaBE54f81970DC8E"
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY", "YOUR_BSCSCAN_KEY")
SUPPORT_HANDLE = "@MANAGEMENTSPORSORSHIP"
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "7214398339"))
except:
    ADMIN_ID = 7214398339

bot = telebot.TeleBot(TOKEN, threaded=True)

# === YOUR ORIGINAL 3 BOTS + 15 NEW BOTS ADDED ===
BOTS = {
    "ma_bot": {"name": "MA Cross PRO EA", "short": "M1 MA Cross - Prop Firm Approved", "price": 399, "reg": 499},
    "gold_bot": {"name": "Gold Scalper Pro", "short": "M1 Gold Scalper - Prop Firm Approved", "price": 799, "reg": 899},
    "rsi_bot": {"name": "RSI Market Master", "short": "M5 RSI Master - All Markets", "price": 549, "reg": 649},
    # NEW BOTS ADDED - PLENTY
    "gold_v5": {"name": "🔥 GOLD SCALPER PRO V5", "short": "M1 Gold Scalper FTMO/MyFunds Approved", "price": 1299, "reg": 1399},
    "xau_sniper": {"name": "🎯 XAUUSD SNIPER V9", "short": "Gold Sniper 95% Accuracy Best Seller", "price": 1799, "reg": 1899},
    "prop_master": {"name": "🏦 PROP FIRM MASTER EA", "short": "Pass FTMO Funding Pips in 7 Days", "price": 2399, "reg": 2499},
    "us30_killer": {"name": "💀 US30 KILLER BOT", "short": "US30 / Dow Jones $50 to $500 Strategy", "price": 1699, "reg": 1799},
    "nas100": {"name": "🚀 NAS100 SCALPER PRO", "short": "NASDAQ High Volatility Profit", "price": 1599, "reg": 1699},
    "eur_break": {"name": "💶 EURUSD BREAKOUT V3", "short": "London Session Breakout", "price": 899, "reg": 999},
    "bollinger": {"name": "🔵 BOLLINGER REVERSAL", "short": "Bollinger Bands Reversal System", "price": 999, "reg": 1099},
    "martingale": {"name": "♻️ MARTINGALE RECOVERY PRO", "short": "Safe Martingale with Recovery", "price": 1199, "reg": 1299},
    "hedge_grid": {"name": "🔷 HEDGE GRID SYSTEM", "short": "Grid + Hedge No Loss Strategy", "price": 1399, "reg": 1499},
    "crypto_scalp": {"name": "₿ CRYPTO SCALPER PRO", "short": "BTC ETH SOL Auto Scalping", "price": 1099, "reg": 1199},
    "btc_sniper": {"name": "₿ BITCOIN SNIPER EA", "short": "BTCUSD M5 Sniper", "price": 1299, "reg": 1399},
    "ict_smc": {"name": "🧠 ICT SMART MONEY V2", "short": "ICT & SMC Order Block FVG", "price": 1899, "reg": 1999},
    "smc_adv": {"name": "💎 SMC ADVANCED PRO", "short": "Order Block FVG Liquidity Grab", "price": 2099, "reg": 2199},
    "news_trader": {"name": "📰 NEWS TRADER PRO", "short": "Auto Trade High Impact News", "price": 1499, "reg": 1599},
    "auto_profit": {"name": "💰 AUTO PROFIT 3.0 AI", "short": "Full Auto AI Set & Forget", "price": 2899, "reg": 2999},
}

pending_payments = {}
paid_tx = set()

# AUTO CHECK EVERY 30 SEC - ANTI FAKE ALERT
def check_payments():
    print("Auto check started - every 30 sec")
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
                            if abs(value - order["price"]) < 1:
                                paid_tx.add(tx_hash)
                                b = BOTS[order["bot_id"]]
                                try:
                                    bot.send_message(user_id, f"✅ PAYMENT CONFIRMED ON-CHAIN!\n\nAmount: ${value}\nTX: {tx_hash}\n\nYour {b['name']} file is being delivered...")
                                    bot.send_message(user_id, f"🎉 DELIVERED: {b['name']}\nThanks for your purchase!")
                                    bot.send_message(ADMIN_ID, f"✅ AUTO PAID! User {user_id} paid ${value} for {b['name']}\nTX: {tx_hash}")
                                    del pending_payments[user_id]
                                except: pass
        except Exception as e:
            print(f"Auto check error: {e}")
        time.sleep(30)

Thread(target=check_payments, daemon=True).start()

@bot.message_handler(commands=['start','shop'])
def start(m):
    welcome_text = (
        f"🏦 FXSTORE - PREMIUM FOREX BOTS\n\n"
        f"Trusted by 3,200+ Traders Worldwide\n\n"
        f"✨ Limited Offer: $100 OFF All Bots\n"
        f"⚡ Instant Auto-Delivery (30 seconds)\n"
        f"🔒 Verified & Secure Payments\n"
        f"🛡️ 30-Day Refund Guarantee\n\n"
        f"⚠️ SCAM ALERT PROTECTION:\n"
        f"We NEVER DM you first. Our only official wallet is the one shown after you select a bot. Beware of impersonators.\n\n"
        f"⚠️ RISK DISCLAIMER:\n"
        f"Trading involves substantial risk of loss. Past performance is not guarantee of future results. Trade at your own risk.\n\n"
        f"Please select your trading bot below to proceed:"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bot_id, b in BOTS.items():
        markup.add(types.InlineKeyboardButton(f"🤖 {b['name']} - ${b['price']} (Reg. ${b['reg']})", callback_data=f"buy_{bot_id}"))
    bot.send_message(m.chat.id, welcome_text, reply_markup=markup)

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
                payment_text = (
                    f"🤖 {b['name']}\n"
                    f"📊 {b['short']}\n\n"
                    f"💰 Price: ${b['price']} ~~${b['reg']}~~\n"
                    f"You Save: $100\n"
                    f"--------------------------------\n"
                    f"💳 PAYMENT INSTRUCTIONS\n\n"
                    f"Please send EXACTLY ${b['price']} USDT (BEP20) to:\n\n"
                    f"`{USDT_ADDRESS}`\n\n"
                    f"⚠️ Important:\n"
                    f"• Network: BSC (BEP20) ONLY\n"
                    f"• Send exact amount to auto-verify\n"
                    f"• Our system monitors the blockchain 24/7\n"
                    f"• Delivery is automatic within 30-60 seconds after payment\n\n"
                    f"⚪ Once payment is detected, your file will be delivered instantly.\n\n"
                    f"🛡️ REFUND POLICY:\n"
                    f"If bot is not delivered automatically after payment, we refund FULL amount within 1 minute. Contact support.\n\n"
                    f"⚠️ RISK WARNING: Trading FOREX/GOLD/CRYPTO involves risk. Our EAs do not guarantee profit. Use proper risk management.\n\n"
                    f"Need help? Contact: {SUPPORT_HANDLE}"
                )
                bot.send_message(call.message.chat.id, payment_text, parse_mode="Markdown")
                bot.send_message(ADMIN_ID, f"🔔 New order pending\nUser: {uid} @{call.from_user.username}\nBot: {b['name']} ${b['price']}\nWaiting auto verify...")
    except Exception as e:
        print(e)

@bot.message_handler(commands=['support','help','refund'])
def support(m):
    bot.send_message(m.chat.id, f"Need help? Contact {SUPPORT_HANDLE}\n\n🛡️ If bot not delivered after payment, we refund within 1 minute.\n\n⚠️ Trading involves risk of loss.")

print("Bot polling...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
