import os
from typing import List, Dict, Union
import discord

from classes import RaidMember, Loot, Reminder
import dill


def get_hash(guild, channel):
    return hash(str(guild) + str(channel))


class RaidDatabase:
    guild: int
    channel: int
    members: Dict[RaidMember]
    reminders: List[Reminder]

    def __init__(self, guild: int, channel: int):
        self.guild = guild
        self.channel = channel
        self.members = {}
        self.reminders = []

    def get_member(self, name) -> RaidMember:
        if name not in self.members[name]:
            self.add_member(name)

        return self.members[name]

    def add_member(self, name):
        self.members[name] = RaidMember(name=name, obtained_loot=Loot())

    def add_reminder(self, ctx, timestamp):
        self.reminders.append(Reminder(time=timestamp, ctx=ctx))


class Database:
    raids: Dict[int, RaidDatabase]
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
            self.raids = dill.load(self.path_to_save)

    def get(self, ctx: discord.Message) -> RaidDatabase:
        guild = ctx.guild.name
        channel = ctx.channel

        hx = get_hash(guild, channel)

        if hx not in self.raids:
            db = RaidDatabase(guild, channel)
            self.raids[hx] = db

            return db

        return self.raids[hx]
