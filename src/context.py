import os
import json

from datetime import datetime

from telegram.ext import ContextTypes

class TheHabbitContext(ContextTypes.DEFAULT_TYPE):
    USER_DATABASE_PATH = "./db"

    @property
    def user_id(self):
        return self.user_data["id"]

    @property
    def user_name(self):
        return self.user_data["name"]

    @property
    def user_file_path(self):
        return f"{self.USER_DATABASE_PATH}/{self.user_id}.json"
        
    @property
    def user_fd(self):
        if "user_fds" not in self.bot_data.keys():
            self.bot_data["user_fds"] = []

        if "fd" not in self.user_data.keys():
            user_fd = open(self.user_file_path, "a+")
            self.bot_data["user_fds"].append(user_fd)
            self.user_data["fd"] = user_fd

            if os.stat(self.user_file_path).st_size == 0:
                json.dump(
                    {
                        "username": self.user_name,
                        "join_date": datetime.today().strftime("%d/%m/%Y")
                    },
                    user_fd,
                    indent=4
                )

        print(self.bot_data["user_fds"])
        return self.user_data["fd"]
