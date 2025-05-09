import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Merhaba! Web3D botu çalışıyor...\nFiyat için /fiyat yazabilirsin.")

async def fiyat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://www.coinstore.com/spot/WEB3DUSDT"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"class": "symbol-last"})
        if price_tag:
            price = price_tag.text.strip()
            await update.message.reply_text(f"Web3D Fiyatı: {price} USDT")
        else:
            await update.message.reply_text("Fiyat bulunamadı.")
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fiyat", fiyat))
    app.run_polling()
