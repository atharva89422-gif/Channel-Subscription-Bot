
# telegram_subscription_bot.py
# Install:
# pip install pyTelegramBotAPI razorpay flask

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import razorpay
from flask import Flask, request

BOT_TOKEN = "PASTE_BOT_TOKEN"
RAZORPAY_KEY_ID = "PASTE_KEY_ID"
RAZORPAY_KEY_SECRET = "PASTE_KEY_SECRET"
CHANNEL_LINK = "https://t.me/your_private_channel"

bot = telebot.TeleBot(BOT_TOKEN)
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
app = Flask(__name__)

plans = {
    "1day": {"amount": 1000, "name": "1 Day"},     # ₹10 (paise)
    "15days": {"amount": 4900, "name": "15 Days"}, # ₹49
    "1month": {"amount": 9900, "name": "1 Month"}  # ₹99
}

@bot.message_handler(commands=['start'])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("1 Day", callback_data="1day"),
        InlineKeyboardButton("15 Days", callback_data="15days"),
        InlineKeyboardButton("1 Month", callback_data="1month")
    )
    bot.send_message(
        message.chat.id,
        "Choose your subscription plan:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data in plans)
def buy(call):
    plan = plans[call.data]

    payment_link = client.payment_link.create({
        "amount": plan["amount"],
        "currency": "INR",
        "description": plan["name"] + " Subscription"
    })

    bot.send_message(
        call.message.chat.id,
        f"Pay here:\n{payment_link['short_url']}"
    )

@app.route('/payment-success', methods=['POST'])
def payment_success():
    data = request.json
    # Add verification/database logic here
    print("Payment received:", data)
    return {"status":"ok"}

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()
