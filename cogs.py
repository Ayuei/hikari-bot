import discord
from discord.ext import commands, tasks
from database import Database, RaidDatabase



class ReminderCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, database: RaidDatabase):
        self.bot = bot
        self.database = database
        self.reminder.start()
        self.passed = False  # 3 cases, what if start up and already passed

    def cog_unload(self):
        self.reminder.cancel()

    @tasks.loop(seconds=30)
    async def reminder(self):
        for r in self.database.reminders:
            hours = r.countdown//3600
            minutes = (hours*3600-r.countdown) // 60
            channel = await self.bot.get_channel(r.channel)
            await channel.send(f"Time until raid: {r.countdown//3600} hours, {(r.countdown % 3600)} minutes.")


class DatabaseCog(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.save_database.start()

    def cog_unload(self):
        self.save_database.cancel()

    @tasks.loop(seconds=10)
    async def save_database(self):
        self.database.save("database.temp")
        self.database.save()


cogs = [ReminderCog, DatabaseCog]
