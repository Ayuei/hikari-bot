import os
from typing import List, Dict, Union
import discord

from classes import RaidMember, Loot, Reminder, BiSPriority
import dill


def get_hash(guild, channel):
    return hash(str(guild) + str(channel))


class RaidDatabase:
    channel: int
    members: Dict[str, RaidMember]
    reminders: Dict[str, Reminder]

    def __init__(self, channel: int):
        self.channel = channel
        self.members = {}
        self.reminders = {}

    def get_member(self, name) -> RaidMember:
        if name not in self.members:
            self.add_member(name)

        return self.members[name]

    def has_reminder(self):
        return len(self.reminders) > 0

    def add_member(self, name):
        loot = Loot()
        self.members[name] = RaidMember(name=name, obtained_loot=loot, bis=BiSPriority(loot))

    def add_reminder(self, ctx, timestamp):
        if timestamp in self.reminders:
            return False

        reminder = Reminder(time=timestamp, ctx=ctx)
        self.reminders[timestamp] = reminder

        return reminder

    def get_reminders(self):
        return self.reminders

    def remove_reminder(self, timestamp):
        try:
            del self.reminders[timestamp]
        except KeyError:
            pass


class Database:
    raids: Dict[str, RaidDatabase]
    path_to_save: str = "database.dill"

    def __init__(self):
        self.raids = {}

    def save(self, path_to_save: str = None):
        if not path_to_save:
            path_to_save = self.path_to_save

        dill.dump(self.raids, open(path_to_save, "wb+"))

    def load(self, path: str = None):
        if not path:
            path = self.path_to_save

        if os.path.exists(path):
            self.raids = dill.load(open(self.path_to_save, "rb"))

    def get(self, ctx: discord.Message) -> RaidDatabase:
        guild = ctx.guild.id
        channel = ctx.channel.id

        hx = str(channel)

        if hx not in self.raids:
            db = RaidDatabase(channel)
            self.raids[hx] = db

            return db

        return self.raids[hx]
