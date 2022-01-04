import dataclasses
import discord
import datetime
from typing import List


class Loot:
    def __init__(self):
        self.head = 0
        self.weapon = 0
        self.chest = 0
        self.glove = 0
        self.pant = 0
        self.boot = 0
        self.earring = 0
        self.necklace = 0
        self.bracelet = 0
        self.ring = 0

    def add_gear(self, gear_to_add: str):
        if gear_to_add.endswith("s"):
            gear_to_add = gear_to_add.rstrip("s").lower()

        gear_attr = getattr(self, gear_to_add)
        setattr(self, gear_to_add, gear_attr+1)

    def remove_gear(self, gear_to_remove: str):
        if gear_to_remove.endswith("s"):
            gear_to_remove = gear_to_remove.rstrip("s").lower()

        gear_attr = getattr(self, gear_to_remove)
        setattr(self, gear_to_remove, gear_attr - 1)


    @classmethod
    def get_gear_count(cls, gear_dict):
        return sum(gear_dict.values())

    def to_dict(self):
        return_dict = {}

        for attr in dir(self):
            # Skip private class variables and non-integers
            if not attr.startswith("__") and not isinstance(attr, int):
                loot_attr = getattr(self, attr)
                if isinstance(loot_attr, int):
                    return_dict[attr] = loot_attr

        return return_dict

    def purge(self):
        for attr in dir(self):
            # Skip private class variables and non-integers
            if not attr.startswith("__") and not isinstance(attr, int):
                setattr(self, attr, 0)


@dataclasses.dataclass(init=True)
class RaidMember:
    name: discord.User.id
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
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class Reminder:
    time: datetime.datetime

    def __init__(self, time: str, ctx: discord.Message):
        days = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6
        }

        self.time = datetime.datetime.strptime(time, "%a %H:%M GMT%z")
        self.day = days[time.split()[0].lower()]

        self.channel = ctx.channel.id
        self.hour_buffer = 8
        self.next_reminder_day = None
        self.last_reminder = None

    # Returns seconds
    def get_countdown(self) -> datetime.timedelta:
        time = self.time

        if self.next_reminder_day is None or self.next_reminder_day > datetime.datetime.now(tz=self.time.tzinfo):
            next_reminder_day = next_weekday(datetime.datetime.now(), self.day)
            self.next_reminder_day = next_reminder_day.replace(hour=time.hour, minute=time.minute,
                                                               tzinfo=self.time.tzinfo)

        countdown = (self.next_reminder_day - datetime.datetime.now(tz=self.time.tzinfo))

        print(countdown)
        print(countdown.days)
        if countdown.days < 0:
            countdown = countdown + datetime.timedelta(days=7)

        return countdown

    def should_remind(self):
        delta = self.get_countdown()
        if self.last_reminder is None:
            if delta.total_seconds()//3600 < self.hour_buffer:
                return True
            return False

        num_days = (datetime.datetime.now() - self.last_reminder).days

        if num_days > 5 and self.get_countdown().total_seconds()//3600 < self.hour_buffer:
            return True

    def purge(self):
        countdown = None
