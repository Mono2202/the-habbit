import os

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def set_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("image", "Send a sample image"),
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your habit tracker bot.")

async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(".\\assets\\golbat.png", "rb") as img:
        await update.message.reply_photo(photo=img, caption="Here's your image!")

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", send_image))
    app.run_polling()

if __name__ == "__main__":
    main()
