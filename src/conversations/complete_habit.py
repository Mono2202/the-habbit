# TODO: when do i give reward? for each frequency? for breaking a habit? when changing the history
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes, CommandHandler
from telegram.constants import ParseMode

from the_habbit import Habit, User
from utils import user_state, cancel

CHANGE_HABIT_STATUS = range(1)

@user_state
async def complete_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    habit_index = int(query.data.split(":", 1)[1])
    habit = context.user.habits[habit_index]

    if (habit.steps <= 0):
        await query.message.reply_text(f"`Breaking` a habit can't be completed, only when the time comes! ⏳", parse_mode=ParseMode.MARKDOWN)

    else:
        habit.status = habit.steps
        await _is_reward(context.user, habit, query.message)

@user_state
async def complete_habit_handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    habit_index = int(query.data.split(":", 1)[1])
    context.user_data["habit_index"] = habit_index

    await query.message.reply_text("Change the current `status` (Insert amount of steps)", parse_mode=ParseMode.MARKDOWN)
    return CHANGE_HABIT_STATUS

@user_state
async def complete_habit_receive_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: maybe change key value to `complete_habit` to match the current module (do to all modules)
    habit = context.user.habits[context.user_data["habit_index"]]
    habit_status_delta = int(update.message.text)

    habit.status += habit_status_delta
    await _is_reward(context.user, habit, update.message)

    return ConversationHandler.END

async def _is_reward(user: User, habit: Habit, message):
    if habit.rewarded and habit.status < habit.steps:
        user.xp -= habit.points
        habit.rewarded = False

    # TODO: maybe i should add to habit creation if its build a habit or break a habit
    if not habit.rewarded and habit.steps > 0 and habit.status >= habit.steps:
        user.xp += habit.points
        habit.rewarded = True

        await message.reply_text(f"🎉🎊🍾 Good job! You got {habit.points} XP ->   `{user.xp}/<NEXT_LEVEL_XP>`", parse_mode=ParseMode.MARKDOWN)

def complete_habit_get_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(complete_habit_handle_button, pattern=r"^status:")],
        states={
            CHANGE_HABIT_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, complete_habit_receive_status)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
