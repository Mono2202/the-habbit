from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes, CommandHandler

from user import User, Habit
from utils import user_state, cancel

ADD_HABIT_NAME, ADD_HABIT_ICON, CHOOSE_HABIT_FREQUENCY, SET_HABIT_POINTS = range(4)

FREQUENCIES = [
    "Daily",
    "Weekly",
    "BiWeekly",
    "Monthly",
]

@user_state
async def add_habit_handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("What's the name of the habit you want to add?")
    return ADD_HABIT_NAME

@user_state
async def add_habit_receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["habit_name"] = update.message.text
    await update.message.reply_text("Choose an icon")
    return ADD_HABIT_ICON

@user_state
async def add_habit_receive_icon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["habit_icon"] = update.message.text
    keyboard = []
    for frequency in FREQUENCIES:
        keyboard.append([
            InlineKeyboardButton(frequency, callback_data=f"frequency:{frequency}")
        ])
    reply_markup = InlineKeyboardMarkup(keyboard)    
    await update.message.reply_text("Frequencies", reply_markup=reply_markup)
    return CHOOSE_HABIT_FREQUENCY

@user_state
async def add_habit_receive_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["habit_frequency"] = query.data.split(":", 1)[1]

    await query.message.reply_text("How many points?")
    return SET_HABIT_POINTS

@user_state
async def add_habit_receive_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["habit_points"] = int(update.message.text)

    context.user.habits.append(Habit(
        name=context.user_data["habit_name"],
        icon=context.user_data["habit_icon"],
        frequency=context.user_data["habit_frequency"],
        points=context.user_data["habit_points"],
    ))

    await update.message.reply_text("Habit added successfully!")

def add_habit_get_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(add_habit_handle_button, pattern="add")],
        states={
            ADD_HABIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_name)],
            ADD_HABIT_ICON: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_icon)],
            CHOOSE_HABIT_FREQUENCY: [CallbackQueryHandler(add_habit_receive_frequency, pattern=r"^frequency:")],
            SET_HABIT_POINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_receive_points)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
