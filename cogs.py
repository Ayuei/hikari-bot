from discord.ext import commands, tasks
from database import Database


class ReminderCog(commands.Cog):
    def __init__(self, bot, database: Database):
        self.bot = bot
        self.database = database
        self.reminder.start()
        self.passed = False  # 3 cases, what if start up and already passed

    def cog_unload(self):
        self.reminder.cancel()

    @tasks.loop(minutes=5)
    async def reminder(self):
        for r in self.database.reminders:
            self.bot.send()


class DatabaseCog(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.save_database.start()

    def cog_unload(self):
        self.save_database.cancel()

    @tasks.loop(minutes=5)
    async def save_database(self):
        self.bot.send()
