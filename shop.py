@bot.message_handler(commands=['start','shop'])
def start(m):
    text = (
        f"🏦 FXSTORE - PREMIUM FOREX BOTS\n"
        f"Trusted by 3,200+ Traders Worldwide\n\n"
        f"✨ Limited Offer: $100 OFF All Bots\n"
        f"⚡ Instant Auto-Delivery (30 seconds)\n"
        f"🔒 Verified & Secure Payments\n"
        f"🛡️ 30-Day Refund Guarantee\n\n"
        f"⚠️ SCAM ALERT PROTECTION:\n"
        f"We NEVER DM you first. Our only official wallet is the one shown after you select a bot. Beware of impersonators. No staff will ask for payment in DM.\n\n"
        f"⚠️ RISK DISCLAIMER:\n"
        f"Trading FOREX, GOLD, CRYPTO & INDICES involves substantial risk of loss. Past performance is not guarantee of future results. Our EAs do not guarantee profit. Trade at your own risk and use proper risk management.\n\n"
        f"Please select your bot below (22 Bots Available):"
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
                    f"💳 PAYMENT INSTRUCTIONS\n\n"
                    f"Send EXACTLY ${b['price']} USDT \\(BEP20\\) to:\n\n"
                    f"`{USDT_ADDRESS}`\n\n"
                    f"⚠️ Important:\n"
                    f"• Network: BSC \\(BEP20\\) ONLY\n"
                    f"• Send exact amount to auto-verify\n"
                    f"• System monitors blockchain 24/7\n"
                    f"• Delivery automatic 30-60 secs after payment\n\n"
                    f"⚠️ SCAM ALERT PROTECTION:\n"
                    f"We NEVER DM first. This is the ONLY official wallet. Beware of fake accounts impersonating us.\n\n"
                    f"🛡️ REFUND POLICY:\n"
                    f"If bot is not delivered automatically after payment, we refund FULL amount within 1 minute. Contact support.\n\n"
                    f"⚠️ RISK WARNING:\n"
                    f"Trading FOREX/GOLD/CRYPTO involves substantial risk of loss. Past performance does not guarantee future results. Our EAs do not guarantee profit. Use proper risk management. Trade at your own risk.\n\n"
                    f"Need help? Contact: {SUPPORT_HANDLE}"
                )
                bot.send_message(c.message.chat.id, msg, parse_mode="Markdown")
                bot.send_message(ADMIN_ID, f"🔔 New order pending\nUser: {uid} @{c.from_user.username}\nBot: {b['name']} ${b['price']}")
    except Exception as e: print(e)
