import os
import json

from datetime import datetime
from telegram import Update

from context import TheHabbitContext

async def start(update: Update, context: TheHabbitContext):
    context.user_data["id"] = update.effective_user.id
    context.user_data["name"] = update.effective_user.name

    await update.message.reply_text(f"Welcome {context.user_name} to The Habbit!")

async def add_habit(update: Update, context: TheHabbitContext):
    print(context.user_fd)
    print(context.user_data)
