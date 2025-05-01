from typing import Callable
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from user import User, Habit

class Command():
    def __init__(self, function: Callable, description: str):
        self.function = function
        self.name = function.__name__
        self.description = description

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Welcome *{context.user.username}* to  `The Habbit`  🧙‍♂️🪄!", parse_mode=ParseMode.MARKDOWN)

async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add exception handling
    context.user.habits.append(Habit(
        name=context.args[0],
        frequency=context.args[1],
        points=context.args[2]
    ))
    await update.message.reply_text(f"✅ Habit `{context.args[0]}` saved successfully!", parse_mode=ParseMode.MARKDOWN)

async def list_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habits_list = ""
    for i, habit in enumerate(context.user.habits):
        habits_list += rf"*{i}. {habit.name}* \[{habit.frequency}, {habit.points} pts]"
        habits_list += "\n"
    await update.message.reply_text(habits_list, parse_mode=ParseMode.MARKDOWN)

async def remove_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add input check
    try:
        habit_index = int(context.args[0])
        removed_habit = context.user.habits[habit_index]
        del context.user.habits[habit_index]
        await update.message.reply_text(f"🗑️ Habit `{removed_habit.name}` removed!", parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await update.message.reply_text(f"❌ Invalid command", parse_mode=ParseMode.MARKDOWN)

COMMANDS = [
    Command(start, "Starts the bot"),
    Command(add_habit, "Adds a new habit"),
    Command(remove_habit, "Removes a habit"),
    Command(list_habits, "List all habits"),
]
