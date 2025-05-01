from typing import Callable
from telegram import Update
from telegram.ext import ContextTypes

class Command():
    def __init__(self, function: Callable, description: str):
        self.function = function
        self.name = function.__name__
        self.description = description

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome {context.user.username} to The Habbit!")

async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user)

COMMANDS = [
    Command(start, "Starts the bot"),
    Command(add_habit, "Adds a new habit"),
]
