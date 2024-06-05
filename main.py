import requests
import time
import telebot

# Manual setup for Telegram bot token and channel ID
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL_ID = "YOUR_TELEGRAM_CHANNEL_ID"

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Cryptocurrency API URL
CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network&vs_currencies=usd'

# Price change intervals
BTC_INTERVAL = 100
ETH_INTERVAL = 10
TON_INTERVAL = 0.02

# Images URLs for each cryptocurrency
IMAGE_URLS = {
    'bitcoin': 'https://files.catbox.moe/wx6i7l.png',
    'ethereum': 'https://files.catbox.moe/fmviuv.png',
    'the-open-network': 'https://files.catbox.moe/8qyxyc.png'
}


def get_crypto_prices():
    response = requests.get(CRYPTO_API_URL)
    data = response.json()

    prices = {}
    for crypto in ['bitcoin', 'ethereum', 'the-open-network']:
        if crypto in data:
            prices[crypto] = data[crypto]['usd']

    return prices

def send_alert(crypto, price):
    message = f'{crypto.upper()} price is now ${price:.2f}'
    image_url = IMAGE_URLS[crypto]
    bot.send_photo(CHANNEL_ID, image_url, caption=message)

def main():
    last_prices = {'bitcoin': None, 'ethereum': None, 'the-open-network': None}

    while True:
        current_prices = get_crypto_prices()

        for crypto in current_prices:
            if last_prices[crypto] is None:
                last_prices[crypto] = current_prices[crypto]
                continue

            price_change = abs(current_prices[crypto] - last_prices[crypto])
            if (crypto == 'bitcoin' and price_change >= BTC_INTERVAL) or \
               (crypto == 'ethereum' and price_change >= ETH_INTERVAL) or \
               (crypto == 'the-open-network' and price_change >= TON_INTERVAL):
                send_alert(crypto, current_prices[crypto])
                last_prices[crypto] = current_prices[crypto]

        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    main()
