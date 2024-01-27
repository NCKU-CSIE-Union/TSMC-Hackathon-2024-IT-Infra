import asyncio
import os
import threading

import discord
from dotenv import load_dotenv

from ai2.log_analyzer import LLMLogAnalyzer
from bot.bot import DiscordBot
from bot.thread import DiscordThreadManager
from monitor.monitor_runner import MonitorRunner
from monitor.service.cloudrun import CloudRunManager


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


if __name__ == "__main__":
    load_dotenv()
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    discord_dst_channel_id = int(os.getenv("DISCORD_DST_CHANNEL_ID"))
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    log_size = os.getenv("LOG_SIZE", 10)
    service_name = "consumer-latest"

    # init discord client
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    # init discord thread manager
    discord_thread_manager = DiscordThreadManager()

    # init cloudrun manager
    cloudrun_manager = CloudRunManager()

    # inti llm log analyzer
    llm_args = {
        "model_name": "text-bison@001",
        "max_output_tokens": 1024,
        "temperature": 0,
    }
    index_name = "tsmc-hackathon"
    llm_log_analyzer = LLMLogAnalyzer(
        pinecone_api_key=pinecone_api_key, index_name=index_name, llm_args=llm_args
    )

    client = discord.Client(intents=intents)
    monitor_runner = MonitorRunner(
        llm_log_analyzer=llm_log_analyzer,
        client=client,
        channel_id=discord_dst_channel_id,
        discord_thread_manager=discord_thread_manager,
        target_service_name=service_name,
        cloudrun_manager=cloudrun_manager,
        log_size=log_size,
    )

    discord_bot = DiscordBot(
        client=client,
        token=discord_bot_token,
        discord_thread_manager=discord_thread_manager,
        channel_id=discord_dst_channel_id,
        monitor_runner=monitor_runner,
    )

    discord_thread = StoppableThread(target=discord_bot.run)
    discord_thread.start()

    try:
        asyncio.run(monitor_runner.run())
    except KeyboardInterrupt:
        print("\nshutting down...")
    except Exception as e:
        print(e)
        exit(1)
    discord_thread.stop()
    asyncio.run_coroutine_threadsafe(discord_bot.cleanup(), discord_bot.client.loop)
    discord_thread.join(2)
