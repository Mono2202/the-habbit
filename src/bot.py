import os
import asyncio
import json
import csv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, Application, ContextTypes
from telegram.constants import ParseMode

from the_habbit import User, Habit
from commands import COMMANDS, HANDLERS
from utils import USER_DATABASE_PATH, _save_user_data

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TheHabbitBot():
    def __init__(self):
        load_dotenv()
        self._bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self._app = ApplicationBuilder().token(TOKEN).post_init(self._set_commands).build()
        job_queue = self._app.job_queue
        job_start = job_queue.run_repeating(self._habit_history, interval=5)
    
    def run(self):
        self._app.run_polling()
        # self._scheduler = AsyncIOScheduler()
        # # self._scheduler.add_job(self._run_habit_history, "cron", hour=0, minute=0)
        # self._scheduler.add_job(self._habit_history, "interval", seconds=10)
        # self._scheduler.start()

    async def _habit_history(self, context: ContextTypes.DEFAULT_TYPE):
        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=6)
        yesterday_format = yesterday.strftime("%d/%m/%Y")
        print(yesterday.weekday())

        for user_file in os.listdir(USER_DATABASE_PATH):
            if user_file.endswith(".json"):
                user_file_path = f"{USER_DATABASE_PATH}/{user_file}"
                with open(user_file_path, "r") as user_fd:
                    user_data = json.load(user_fd)
                current_user = User(**user_data)

                with open(f"{USER_DATABASE_PATH}/{user_file.split(".json")[0]}.csv", mode="a", newline="", encoding="utf-8") as habit_history_fd:
                    user_message = "Congrats! Today you completed:\n" 
                    writer = csv.writer(habit_history_fd)
                    for habit in current_user.habits:
                        if habit.frequency == "Daily" or (today.weekday() == 6 and habit.frequency == "Weekly") or (today.day == 1 and habit.frequency == "Monthly"):
                            if habit.status >= habit.steps and not habit.rewarded:
                                current_user.xp += habit.points 
                                habit.rewarded = True
                            writer.writerow(
                                [
                                    yesterday_format,
                                    habit.name,
                                    habit.icon,
                                    habit.steps,
                                    habit.unit,
                                    habit.frequency,
                                    habit.points,
                                    habit.status,
                                    habit.rewarded
                                ]
                            )
                            if habit.rewarded:
                                user_message += f"{habit.name} {habit.icon} -> `+{habit.points} XP`\n"
                            # TODO: add else, message for uncompleted tasks, at the top condition?
                            # TODO: add current level after gaining xp
                            habit.status = 0
                            habit.rewarded = False
                
                await self._app.bot.send_message(chat_id=current_user.id, text=user_message, parse_mode=ParseMode.MARKDOWN)
                _save_user_data(current_user) 
                

    @staticmethod
    async def _set_commands(app: Application):
        bot_commands = []

        for handler in HANDLERS:
            app.add_handler(handler)

        for command in COMMANDS:
            app.add_handler(
                CommandHandler(
                    command.name,
                    command.function
                )
            )

            bot_commands.append(
                BotCommand(
                    command.name,
                    command.description
                )
            )

        await app.bot.set_my_commands(bot_commands)
