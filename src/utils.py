import os
import json

from typing import Callable
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime

from user import User

USER_DATABASE_PATH = "./db"

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled")
    return ConversationHandler.END

def user_state(func: Callable):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = _get_user_data(update.effective_user.id, update.effective_user.name)
        context.user = user

        return_value = await func(update, context, *args, **kwargs)

        _save_user_data(user) 
        return return_value
    return wrapper

def _save_user_data(user: User):
    user_file_path = f"{USER_DATABASE_PATH}/{user.id}.json"
    with open(user_file_path, "w") as user_fd:
        user_fd.write(user.model_dump_json(indent=4))

def _get_user_data(user_id: int, user_name: str):
    user_file_path = f"{USER_DATABASE_PATH}/{user_id}.json"
    if not os.path.exists(user_file_path):
        user = User(
            id=user_id,
            username=user_name,
            join_date=datetime.today().strftime("%d/%m/%Y"),
            habits=[]
        )
        _save_user_data(user)
        return user

    with open(user_file_path, "r") as user_fd:
        user_data = json.load(user_fd)
    return User(**user_data)
