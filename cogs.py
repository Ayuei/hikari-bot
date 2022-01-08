import datetime

import discord
from discord.ext import commands, tasks
from database import Database, RaidDatabase


class ReminderCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, database: Database):
        self.bot = bot
        self.database = database
        self.reminder.start()
        self.passed = False  # 3 cases, what if start up and already passed

    def cog_unload(self):
        self.reminder.cancel()

    @tasks.loop(seconds=30)
    async def reminder(self):
        for raid in self.database.raids.values():
            if raid.has_reminder():
                for raid_reminder in raid.reminders.values():
                    time_delta = raid_reminder.get_countdown()
                    if raid_reminder.should_remind():
                        hours = int(time_delta.seconds // 3600)
                        minutes = int((time_delta.seconds % 3600) // 60)

                        channel = self.bot.get_channel(raid_reminder.channel)

                        await channel.send(f"Raid Reminder! Time until raid: {hours} hours, "
                                           f"{minutes} minutes.")

                        raid_reminder.last_reminder = datetime.datetime.now()
                        raid_reminder.alarm = False

                    if time_delta.total_seconds() < 30 and raid_reminder.alarm:
                        channel = self.bot.get_channel(raid_reminder.channel)
                        await channel.send(f"Gamers, it's time for raid owo!")
                        raid_reminder.alarm = False


class DatabaseCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, database: Database):
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
