import os
import json

from datetime import datetime

from telegram.ext import ContextTypes

USER_DATABASE_PATH = "db"

class TheHabbitContext(ContextTypes.DEFAULT_TYPE):
    @property
    def user_id(self):
        return self.user_data["id"]

    @property
    def user_name(self):
        return self.user_data["name"]

    @property
    def user_file_path(self):
        return f"{USER_DATABASE_PATH}/{self.user_id}.json"
        
    @property
    def user_file(self):
        if "fd" not in self.user_data.keys():
            self.user_data["fd"] = open(self.user_file_path, "a+")
            if os.stat(self.user_file_path).st_size == 0:
                json.dump(
                    {
                        "username": self.user_name,
                        "join_date": datetime.today().strftime("%d/%m/%Y")
                    },
                    self.user_data["fd"],
                    indent=4
                )
        return self.user_data["fd"]
