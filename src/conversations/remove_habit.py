from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes, CommandHandler
from telegram.constants import ParseMode

from user import Habit
from utils import user_state, cancel

REMOVE_HABIT = range(1)

@user_state
async def remove_habit_handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["habit_to_remove_index"] = int(query.data.split(":", 1)[1])
    habit = context.user.habits[context.user_data["habit_to_remove_index"]]

    # TODO: can the icon be an actual icon (.ico)? Interesting
    await query.message.reply_text(fr"Are you sure you want to delete `{habit.name} {habit.icon}` \[Respond 'Yes']", parse_mode=ParseMode.MARKDOWN)
    return REMOVE_HABIT

@user_state
async def remove_habit_receive_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habit = context.user.habits[context.user_data["habit_to_remove_index"]]
    if update.message.text == "Yes":
        del context.user.habits[context.user_data["habit_to_remove_index"]]
        await update.message.reply_text(f"❌ Habit `{habit.name} {habit.icon}` deleted successfully!", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"Operation cancelled", parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END

def remove_habit_get_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(remove_habit_handle_button, pattern=r"^remove:")],
        states={
            REMOVE_HABIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_habit_receive_confirmation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
