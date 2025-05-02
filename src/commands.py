from typing import Callable
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from conversations.add_habit import add_habit_get_handler
from conversations.remove_habit import remove_habit_get_handler
from conversations.complete_habit import complete_habit, complete_habit_get_handler

from utils import user_state

class Command():
    def __init__(self, function: Callable, description: str):
        self.function = function
        self.name = function.__name__
        self.description = description

# TODO: build the keyboard of habits
# def build_habits_keyboard():

@user_state
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Welcome *{context.user.username}* to  `The Habbit`  🧙‍♂️🪄!", parse_mode=ParseMode.MARKDOWN)

@user_state
async def list_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for i, habit in enumerate(context.user.habits):
        tools_row = [
            InlineKeyboardButton(f"✅", callback_data=f"complete:{i}"),
            # TODO: edit -> will need to change all of the csv aswell? what about game progression
            InlineKeyboardButton(f"✏️", callback_data=f"edit:{i}"),
            InlineKeyboardButton(f"🗑️", callback_data=f"remove:{i}"),
        ]
        info_row = [
            InlineKeyboardButton(f"{habit.icon} {habit.name}", callback_data=f"info:{i}"),
            InlineKeyboardButton(f"{habit.status} / {habit.steps} {habit.unit} {"🟢" if habit.status >= habit.steps else "️⭕"}", callback_data=f"status:{i}"),
        ]
        keyboard.append(info_row)
        keyboard.append(tools_row)
    keyboard.append([InlineKeyboardButton(f"➕", callback_data="add")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("~~~~~~ Habits ~~~~~~", reply_markup=reply_markup)

@user_state
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
    Command(list_habits, "List all habits"),
]

HANDLERS = [
    CallbackQueryHandler(complete_habit, pattern=r"^complete:"),
    add_habit_get_handler(),
    remove_habit_get_handler(),
    complete_habit_get_handler(),
]
