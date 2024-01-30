import os

import discord
from dotenv import load_dotenv

from monitor.monitor_runner import MonitorRunner

from .feedback import get_active_threads, process_feedback
from .message import send_embedded_message
from .thread import DiscordThreadManager


class DiscordBot:
    def __init__(
        self,
        client: discord.Client,
        token: str,
        channel_id: int,
        monitor_runner: MonitorRunner,
        discord_thread_manager: DiscordThreadManager,
    ):
        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.intents.message_content = True
        self.token = token
        self.channel_id = channel_id
        self.client = client
        # self.active_threads = []
        self.discord_thread_manager = discord_thread_manager
        self.monitor_runner = monitor_runner

    async def update_active_threads(self):
        self.active_threads = await get_active_threads()

    async def on_ready(self):
        print(f"Logged in as {self.client.user}")

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        for thread in self.discord_thread_manager.get_active_threads():
            if message.channel.id == thread.id:
                await self.process_feedback(message, thread)

    async def process_feedback(self, message, thread):
        ai_response = self.monitor_runner.get_agent_response(
            str(thread.id),
            message.content,
        )
        await thread.send(ai_response)

    async def send_alert(self, message_dict: dict):
        channel = self.client.get_channel(self.channel_id)
        if channel:
            try:
                await send_embedded_message(channel, message_dict)
            except Exception as e:
                print("Error sending warning message:", e)

    def run(self):
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.run(self.token)

    async def cleanup(self):
        await self.client.close()


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_DST_CHANNEL_ID = int(os.getenv("DISCORD_DST_CHANNEL_ID"))

last_warning = None
active_threads = []


# 權限設置
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

test_info = {
    "severity": "ERROR",
    "cpu": -1,
    "memory": 0,
    "instance": 1,
    "message": "The application is experiencing high latency and is unable to keep up with the demand. The number of tasks in the queue has been above 100 for the past 5 minutes and the average task execution time has been above 30 seconds. I recommend increasing the number of instances by 1.",
    "timestamp": "2024-01-26 11:05:49+00:00",
    # 'metric_dataframe': pd.DataFrame
}


async def update_active_threads():
    global active_threads
    active_threads = await get_active_threads()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(DISCORD_DST_CHANNEL_ID)
    await channel.send("開始模擬即時資料")
    # channel = client.get_channel(DISCORD_DST_CHANNEL_ID)
    # client.loop.create_task(update_active_threads())
    # if channel:
    #     await send_embedded_message(channel, test_info)

    # await asyncio.sleep(5)
    # await send_embedded_error(channel)
    # await asyncio.sleep(5)
    # await send_embedded_info(channel)


# 監聽討論串訊息
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for thread in active_threads:
        if message.channel.id == thread.id:
            await process_feedback(message, thread)


async def send_alert(message_dict: dict):
    print("broadcasting")
    test_channel_id = DISCORD_DST_CHANNEL_ID
    channel = client.get_channel(test_channel_id)
    if channel:
        try:
            await send_embedded_message(channel, message_dict)
        except Exception as e:
            print("Error sending warning message:", e)


def run_bot():
    # print("TSMC System Bot is Online!")
    client.run(DISCORD_BOT_TOKEN)


# 測試 function
# async def pull_warning():
#     num = random.randint(0,100)
#     return f"編號{num}這是一個新的警告！"

# async def warning_task():
#     global last_warning
#     while True:
#         # 呼叫 pull_warning 函數獲取最新警告
#         new_warning = await pull_warning()
#         if new_warning != last_warning:
#             # 如果新警告與上一次警告不同，則向 Discord 頻道發送新警告
#             last_warning = new_warning
#             channel = client.get_channel(1199372364870340810)
#             await channel.send(new_warning)
#         await asyncio.sleep(5)


# @client.event
# async def on_ready():
#     # print(f'{client.user} has connected to Discord!')
#     # print("TSMC System Bot is Online!")
#     channel = client.get_channel(DISCORD_DST_CHANNEL_ID)
#     await channel.send("開始模擬即時資料")


# client.run(DISCORD_BOT_TOKEN)
