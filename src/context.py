from telegram.ext import ContextTypes

class TheHabbitContext(ContextTypes.DEFAULT_TYPE):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.user_fds = []

    @property
    def user_id(self):
        return self.user_data["id"]

    @property
    def user_name(self):
        return self.user_data["name"]
        
    @property
    def user_file(self):
        return self.user_data["fd"]
