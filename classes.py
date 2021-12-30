import dataclasses
import discord
import datetime
from typing import List


class Loot:
    def __init__(self):
        self.head = 0
        self.weapon = 0
        self.chest = 0
        self.gloves = 0
        self.pants = 0
        self.boots = 0
        self.earrings = 0
        self.necklace = 0
        self.bracelet = 0
        self.ring = 0

    def add_gear(self, gear_to_add: str):
        gear_attr = getattr(self, gear_to_add)
        gear_attr += 1

    @classmethod
    def get_gear_count(cls, gear_dict):
        return sum(gear_dict.values())

    def to_dict(self):
        return_dict = {}

        for attr in dir(self):
            # Skip private class variables and non-integers
            if not attr.startswith("__") and not isinstance(attr, int):
                return_dict[attr] = getattr(self, attr)

        return return_dict

    def purge(self):
        for attr in dir(self):
            # Skip private class variables and non-integers
            if not attr.startswith("__") and not isinstance(attr, int):
                setattr(self, attr, None)


@dataclasses.dataclass(init=True)
class RaidMember:
    name: discord.User.id
    guild: discord.Guild.id
    obtained_loot: Loot

    def to_dict(self):
        return {
            "name": self.name,
            "obtained_loot": self.obtained_loot.to_dict(),
        }

    def purge(self):
        self.obtained_loot.purge()


@dataclasses.dataclass(init=True)
class Raid:
    members: List[RaidMember]

    def to_dict(self):
        return {
            "members": [member.to_dict() for member in self.members]
        }

    def purge(self):
        for member in self.members:
            member.purge()


# https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-date
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class Reminder:
    time: datetime.datetime

    def __init__(self, time: str, ctx: discord.Message):
        self.time = datetime.datetime.strptime(time, "'%A:%H:%M'")
        self.channel = ctx.channel
        self.hour_buffer = 8
        self.countdown = None

    # Returns seconds
    def get_countdown(self) -> int:
        if not self.countdown:
            next_reminder_day = next_weekday(datetime.datetime.now(), self.time.weekday())
            next_reminder_day = next_reminder_day.replace(hour=self.time.hour, minute=self.time.minute)

            self.countdown = (next_reminder_day - datetime.datetime.now()).total_seconds() - self.hour_buffer * 3600

        return self.countdown

    def purge(self):
        self.countdown = None
