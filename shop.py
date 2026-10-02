import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types
import time
import requests

app = Flask(__name__)
@app.route('/')
def home(): return "FOREX BOTS SHOP is Live! UptimeRobot OK"
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN")
USDT_ADDRESS = os.getenv("USDT_ADDRESS", "0x307acAdEE363C72C3F388b0AaBE54f81970DC8E")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7214398339"))
SUPPORT_HANDLE = "@MANAGEMENTSPORSORSHIP"

bot = telebot.TeleBot(TOKEN, threaded=True)

# === 22 BOTS LIST WITH HIGH PRICES - $100 OFF ===
BOTS = {
    "ma_cross": {"name": "MA Cross PRO EA", "short": "M1 MA Cross - Prop Firm Approved", "price": 399, "reg": 499},
    "gold_v5": {"name": "🔥 GOLD SCALPER PRO V5", "short": "M1 Gold Scalper - FTMO Approved", "price": 799, "reg": 899},
    "rsi_master": {"name": "RSI Market Master", "short": "M5 RSI Master - All Markets", "price": 549, "reg": 649},
    "xau_sniper": {"name": "🎯 XAUUSD SNIPER V9", "short": "Gold Sniper 95% Accuracy", "price": 1799, "reg": 1899},
    "prop_master": {"name": "🏦 PROP FIRM MASTER EA", "short": "Pass FTMO in 7 Days - All Prop Firms", "price": 2399, "reg": 2499},
    "us30_killer": {"name": "💀 US30 KILLER BOT", "short": "US30/Dow Jones Scalper", "price": 1699, "reg": 1799},
    "nas100": {"name": "🚀 NAS100 SCALPER PRO", "short": "NASDAQ High Volatility Profit", "price": 1599, "reg": 1699},
    "eur_break": {"name": "💶 EURUSD BREAKOUT V3", "short": "London Session Breakout", "price": 899, "reg": 999},
    "bollinger": {"name": "🔵 BOLLINGER REVERSAL", "short": "Bollinger Reversal System", "price": 999, "reg": 1099},
    "martingale": {"name": "♻️ MARTINGALE RECOVERY PRO", "short": "Safe Martingale Recovery", "price": 1199, "reg": 1299},
    "hedge_grid": {"name": "🔷 HEDGE GRID SYSTEM", "short": "Grid + Hedge No Loss", "price": 1399, "reg": 1499},
    "crypto_scalp": {"name": "₿ CRYPTO SCALPER PRO", "short": "BTC ETH SOL Auto Scalp", "price": 1099, "reg": 1199},
    "btc_sniper": {"name": "₿ BITCOIN SNIPER EA", "short": "BTCUSD M5 Sniper", "price": 1299, "reg": 1399},
    "ict_smc": {"name": "🧠 ICT SMART MONEY V2", "short": "ICT & SMC Order Block FVG", "price": 1899, "reg": 1999},
    "smc_adv": {"name": "💎 SMC ADVANCED PRO", "short": "Advanced SMC Liquidity Grab", "price": 2099, "reg": 2199},
    "news_trader": {"name": "📰 NEWS TRADER PRO", "short": "Auto Trade High Impact News", "price": 1499, "reg": 1599},
    "gbp_scalp": {"name": "💷 GBPUSD SCALPER", "short": "London Killer GBP", "price": 899, "reg": 999},
    "forex_gump": {"name": "🤖 FOREX GUMP ULTRA", "short": "Legendary 10 Years Profitable", "price": 1799, "reg": 1899},
    "forex_diamond": {"name": "💎 FOREX DIAMOND EA", "short": "Trend + Counter-Trend", "price": 1599, "reg": 1699},
    "forex_combo": {"name": "⚙️ FOREX COMBO SYSTEM", "short": "8 Strategies in 1 Portfolio", "price": 2199, "reg": 2299},
    "m5_ultra": {"name": "⚡ M5 SCALPER ULTRA", "short": "M5 Scalper All Pairs", "price": 799, "reg": 899},
    "auto_profit": {"name": "💰 AUTO PROFIT 3.0 AI", "short": "Full Auto AI Set & Forget", "price": 2899, "reg": 2999},
}

pending_payments = {}
paid_tx = set()

def check_payments():
    while True:
        try:
            if not BSCSCAN_API_KEY:
                time.sleep(60)
                continue
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={USDT_ADDRESS}&startblock=0&endblock=99999999&sort=desc&apikey={BSCSCAN_API_KEY}"
            res = requests.get(url, timeout=20).json()
            if res.get("status") == "1":
                for tx in res.get("result", [])[:25]:
                    h = tx.get("hash")
                    if h in paid_tx: continue
                    if tx.get("to","").lower() == USDT_ADDRESS.lower():
                        val = int(tx.get("value",0)) / (10 ** int(tx.get("tokenDecimal",18)))
                        for uid, order in list(pending_payments.items()):
                            if abs(val - order["price"]) < 1 and (time.time() - order["time"] < 3600):
                                paid_tx.add(h)
                                b = BOTS[order["bot_id"]]
                                bot.send_message(uid, f"✅ PAYMENT CONFIRMED ${val}\nTX: {h}\n\nDelivering {b['name']}...")
                                bot.send_message(ADMIN_ID, f"✅ PAID User {uid} ${val} for {b['name']} TX:{h}")
                                del pending_payments[uid]
        except: pass
        time.sleep(30)
Thread(target=check_payments, daemon=True).start()

@bot.message_handler(commands=['start','shop'])
def start(m):
    text = (
        f"🏦 FXSTORE - PREMIUM FOREX BOTS\n"
        f"Trusted by 3,200+ Traders Worldwide\n\n"
        f"✨ LIMITED: $100 OFF ALL BOTS TODAY!\n"
        f"⚡ Instant Auto-Delivery (30 secs)\n"
        f"🔒 Secure USDT BEP20\n"
        f"🛡️ 30-Day Refund Guarantee\n\n"
        f"Select bot below (22 Bots Available):"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bid, b in BOTS.items():
        markup.add(types.InlineKeyboardButton(f"{b['name']} - ${b['price']} (Reg ${b['reg']})", callback_data=f"buy_{bid}"))
    bot.send_message(m.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def handle(c):
    try:
        bot.answer_callback_query(c.id)
        uid = c.from_user.id
        if c.data.startswith("buy_"):
            bid = c.data.replace("buy_","")
            if bid in BOTS:
                b = BOTS[bid]
                pending_payments[uid] = {"bot_id": bid, "price": b["price"], "time": time.time()}
                msg = (
                    f"🤖 *{b['name']}*\n"
                    f"📊 {b['short']}\n\n"
                    f"💰 Price: ${b['price']} ~${b['reg']}~ Save $100\n"
                    f"--------------------------------\n"
                    f"💳 Send EXACTLY ${b['price']} USDT BEP20 to:\n\n"
                    f"`{USDT_ADDRESS}`\n\n"
                    f"Network: BSC BEP20 ONLY\n"
                    f"Auto verify + delivery 30-60 secs\n\n"
                    f"🛡️ Refund if not delivered - Contact {SUPPORT_HANDLE}\n"
                    f"⚠️ Trading involves risk."
                )
                bot.send_message(c.message.chat.id, msg, parse_mode="Markdown")
    except Exception as e: print(e)

print("Bot polling...")
while True:
    try: bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(e)
        time.sleep(5)
