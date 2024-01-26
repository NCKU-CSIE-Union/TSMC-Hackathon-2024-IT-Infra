import os
import threading

import discord
from dotenv import load_dotenv

from bot.bot import DiscordBot
from bot.thread import DiscordThreadManager
from monitor.monitor_runner import FakeChatAI, MonitorRunner
from monitor.service.cloudrun import CloudRunManager

if __name__ == "__main__":
    load_dotenv()
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    discord_dst_channel_id = int(os.getenv("DISCORD_DST_CHANNEL_ID"))
    service_name = "consumer-latest"

    # init chat agent
    fake_chat_ai = FakeChatAI()

    # init discord client
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    # init discord thread manager
    discord_thread_manager = DiscordThreadManager()

    # init cloudrun manager
    cloudrun_manager = CloudRunManager()

    client = discord.Client(intents=intents)
    monitor_runner = MonitorRunner(
        chat_agent=fake_chat_ai,
        client=client,
        channel_id=discord_dst_channel_id,
        discord_thread_manager=discord_thread_manager,
        target_service_name=service_name,
        cloudrun_manager=cloudrun_manager,
    )

    discord_bot = DiscordBot(
        client=client,
        token=discord_bot_token,
        discord_thread_manager=discord_thread_manager,
        channel_id=discord_dst_channel_id,
        monitor_runner=monitor_runner,
    )

    discord_thread = threading.Thread(target=discord_bot.run)
    discord_thread.start()

    monitor_runner.run()
