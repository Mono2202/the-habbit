from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes, CommandHandler
from telegram.constants import ParseMode

from user import Habit
from utils import user_state, cancel

ADD_HABIT_NAME, ADD_HABIT_ICON, CHOOSE_HABIT_FREQUENCY, SET_HABIT_POINTS = range(4)

FREQUENCIES = [
    "Daily",
    "Weekly",
    "BiWeekly",
    "Monthly",
]

# TODO: add input checks for each function

async def add_habit_handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("What's the `name` of the habit you want to add? 🤔", parse_mode=ParseMode.MARKDOWN)
    return ADD_HABIT_NAME

async def add_habit_receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: I could change it to a Habit class, but should I?
    context.user_data["habit_name"] = update.message.text
    await update.message.reply_text("Choose an `icon` for the new habit! 🖼️", parse_mode=ParseMode.MARKDOWN)
    return ADD_HABIT_ICON

async def add_habit_receive_icon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["habit_icon"] = update.message.text
    keyboard = []
    for frequency in FREQUENCIES:
        keyboard.append([
            InlineKeyboardButton(frequency, callback_data=f"frequency:{frequency}")
        ])
    reply_markup = InlineKeyboardMarkup(keyboard)    
    await update.message.reply_text("Choose the `frequency` of the habit 📈", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return CHOOSE_HABIT_FREQUENCY

async def add_habit_receive_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["habit_frequency"] = query.data.split(":", 1)[1]
    await query.message.reply_text(f"You chose: `{context.user_data["habit_frequency"]}` 🥵", parse_mode=ParseMode.MARKDOWN)

    # TODO: maybe change the name from points to something more appealing...
    await query.message.reply_text("How many `points` for completing the habit? 💯", parse_mode=ParseMode.MARKDOWN)
    return SET_HABIT_POINTS

@user_state
async def add_habit_receive_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: limit the points?
    context.user_data["habit_points"] = int(update.message.text)

    context.user.habits.append(Habit(
        name=context.user_data["habit_name"],
        icon=context.user_data["habit_icon"],
        frequency=context.user_data["habit_frequency"],
        points=context.user_data["habit_points"],
    ))

    await update.message.reply_text(f"✅ Habit `{context.user_data["habit_name"]} {context.user_data["habit_icon"]}` added successfully!", parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END

def add_habit_get_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(add_habit_handle_button, pattern=r"^add")],
        states={
            ADD_HABIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_name)],
            ADD_HABIT_ICON: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_icon)],
            CHOOSE_HABIT_FREQUENCY: [CallbackQueryHandler(add_habit_receive_frequency, pattern=r"^frequency:")],
            SET_HABIT_POINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_points)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
