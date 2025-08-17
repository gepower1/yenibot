import os
import telebot
from flask import Flask, request
import requests

TOKEN = "7591570412:AAGJ43nkH6ZZikX6VMJGCXVbpyUxyrDb8OA"  # senin bot token
bot = telebot.TeleBot(TOKEN)

# Flask server
app = Flask(__name__)

# -------------------------
# CoinGecko API
# -------------------------
def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(coin_id, {}).get("usd")

# -------------------------
# Komutlar
# -------------------------
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "👋 Merhaba! Bana bir coin adı (ör: btc, eth, sol) yaz, fiyatını göstereyim.")

@bot.message_handler(func=lambda m: True)
def coin_price(message):
    coin = message.text.lower()
    mapping = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "xrp": "ripple",
        "doge": "dogecoin",
    }
    coin_id = mapping.get(coin, coin)

    price = get_price(coin_id)
    if price:
        bot.reply_to(message, f"💰 {coin.upper()} fiyatı: {price} USD")
    else:
        bot.reply_to(message, f"⚠️ {coin.upper()} bulunamadı.")

# -------------------------
# Flask webhook endpoint
# -------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot çalışıyor 🚀", 200

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
