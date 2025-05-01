import os
import json

from datetime import datetime
from telegram import Update

from context import TheHabbitContext


USER_DATABASE_PATH = "./db"

def open_user_file(user_id: int, context: TheHabbitContext):
    user_file_path = f"{USER_DATABASE_PATH}/{str(user_id)}.json"
    user_fd = open(user_file_path, "a+")
    context.user_fds.append(user_fd)

    if os.stat(user_file_path).st_size == 0:
        json.dump(
            {
                "username": context.user_name,
                "join_date": datetime.today().strftime("%d/%m/%Y")
            },
            user_fd,
            indent=4
        )

    return user_fd

async def start(update: Update, context: TheHabbitContext):
    context.user_data["id"] = update.effective_user.id
    context.user_data["name"] = update.effective_user.name

    user_fd = open_user_file(context.user_id, context)
    context.user_data["fd"] = user_fd

    await update.message.reply_text(f"Welcome {context.user_name} to The Habbit!")

async def add_habit(update: Update, context: TheHabbitContext):
    print(context.user_data)
