from typing import Callable
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

from user import User, Habit

class Command():
    def __init__(self, function: Callable, description: str):
        self.function = function
        self.name = function.__name__
        self.description = description

# TODO: build the keyboard of habits
def build_habits_keyboard():

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Welcome *{context.user.username}* to  `The Habbit`  🧙‍♂️🪄!", parse_mode=ParseMode.MARKDOWN)

async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add exception handling
    context.user.habits.append(Habit(
        name=context.args[0],
        icon=context.args[1],
        frequency=context.args[2],
        points=context.args[3]
    ))
    await update.message.reply_text(f"✅ Habit `{context.args[0]}` saved successfully!", parse_mode=ParseMode.MARKDOWN)

async def list_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for i, habit in enumerate(context.user.habits):
        row = [
            InlineKeyboardButton(f"✅", callback_data=f"complete:{i}"),
            InlineKeyboardButton(f"✏️", callback_data=f"edit:{i}"),
            InlineKeyboardButton(f"✏️", callback_data=f"edit:{i}"),
            InlineKeyboardButton(f"✏️", callback_data=f"edit:{i}"),
        ]
        keyboard.append([InlineKeyboardButton(f"{habit.icon} {habit.name}", callback_data=f"statistics:{i}")])
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("~~~ Habits ~~~", reply_markup=reply_markup)

async def remove_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: add input check
    try:
        habit_index = int(context.args[0])
        removed_habit = context.user.habits[habit_index]
        del context.user.habits[habit_index]
        await update.message.reply_text(f"🗑️ Habit `{removed_habit.name}` removed!", parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await update.message.reply_text(f"❌ Invalid command", parse_mode=ParseMode.MARKDOWN)

async def complete_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    habit_index = int(query.data.split(":", 1)[1])
    await query.edit_message_text(f"You chose: {context.user.habits[habit_index].name}")

COMMANDS = [
    Command(start, "Starts the bot"),
    Command(add_habit, "Adds a new habit"),
    Command(remove_habit, "Removes a habit"),
    Command(list_habits, "List all habits"),
]

QUERY_HANDLERS = [
    CallbackQueryHandler(complete_habit, pattern=r"^complete:")
]
