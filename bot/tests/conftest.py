import pytest

import os

import discord

from ai2.log_analyzer import LLMLogAnalyzer
from bot.bot import DiscordBot
from bot.thread import DiscordThreadManager
from monitor.monitor_runner import MonitorRunner
from monitor.service.cloudrun import CloudRunManager


@pytest.fixture(scope="class")
def discord_bot():
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    discord_dst_channel_id = int(os.getenv("DISCORD_DST_CHANNEL_ID"))
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
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
    )

    discord_bot = DiscordBot(
        client=client,
        token=discord_bot_token,
        discord_thread_manager=discord_thread_manager,
        channel_id=discord_dst_channel_id,
        monitor_runner=monitor_runner,
    )

    return discord_bot
