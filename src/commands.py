from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome {context.user.username} to The Habbit!")

async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user)
