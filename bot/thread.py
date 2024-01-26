from typing import List

import discord


class DiscordThreadManager:
    def __init__(self):
        self.active_threads: List[discord.Thread] = []

    def get_active_threads(self):
        return self.active_threads

    def add_thread(self, thread: discord.Thread):
        self.active_threads.append(thread)
