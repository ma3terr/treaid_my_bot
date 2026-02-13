import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def get_price(coin: str) -> float:
    coin = coin.upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
    data = requests.get(url, timeout=10).json()
    return float(data["price"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام!\n"
        "قیمت رو اینطوری بگیر:\n"
        "/price BTC\n"
        "/price ETH"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("نمونه: /price BTC")
        return

    coin = context.args[0].upper()
    try:
        p = get_price(coin)
        await update.message.reply_text(f"{coin}/USDT = {p:,.4f}")
    except Exception:
        await update.message.reply_text("خطا: نماد نامعتبر یا مشکل اتصال. نمونه: /price BTC")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.run_polling()

if __name__ == "__main__":
    main()
