import os
from typing import List, Dict

from classes import RaidMember, Loot, Reminder
import dill


class Database:
    members: Dict[RaidMember]
    path_to_save: str = "database.dill"
    reminders: List[Reminder]

    def __init__(self):
        self.members = {}
        self.reminders = []

    def get_member(self, name):
        return self.members[name]

    def add_member(self, name):
        self.members[name] = RaidMember(name=name, obtained_loot=Loot())

    def add_reminder(self, time):
        pass

    def save(self):
        dill.dump(self.members, open(self.path_to_save, "wb+"))

    def load(self, path: str = None):
        if not path:
            path = self.path_to_save

        if os.path.exists(path):
            self.members = dill.load(self.path_to_save)
