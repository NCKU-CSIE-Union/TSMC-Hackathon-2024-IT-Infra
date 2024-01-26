import asyncio
import os

import discord
from dotenv import load_dotenv

from feedback import get_active_threads, process_feedback
from message import send_embedded_message

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
    "message": "The application is experiencing errors. The following errors have been detected:\n\n* Failed response detected 19 times over the last 5 minutes.\n\nThe potential cause of the error is that the application is not able to handle the load. This could be due to a number of factors, such as:\n\n* The application is not scalable.\n* The application is not using the correct resources.\n* The application is not properly configured.\n\nTo fix the error, you should:\n\n* Review the application's architecture and make sure that it is scalable.\n* Review the application's resource usage and make sure that it is using the correct resources.\n* Review the application's configuration and make sure that it is properly configured.\n\nIf you are unable to fix the error, you should contact Google Cloud support for assistance.",
    # "metric_dataframe": pd.DataFrame,
    "timestamp": "Thu Dec 07 2023 09:04:00"
}


async def update_active_threads():
    global active_threads
    active_threads = await get_active_threads()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(DISCORD_DST_CHANNEL_ID)
    client.loop.create_task(update_active_threads())
    if channel:
        await send_embedded_message(channel, test_info)
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


# async def broadcast(message_dict: dict):
#     print("broadcasting")
#     test_channel_id = 1199372364870340810
#     channel = client.get_channel(test_channel_id)
#     if channel:
#         try:
#             await send_embedded_warning(channel, message_dict["message"])
#         except Exception as e:
#             print("Error sending warning message:", e)
#         await asyncio.sleep(5)


# def run_bot():
#     print("TSMC System Bot is Online!")
#     client.run(DISCORD_BOT_TOKEN)


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
#     print(f'{client.user} has connected to Discord!')
#     print("TSMC System Bot is Online!")
#     client.loop.create_task(warning_task())


client.run(DISCORD_BOT_TOKEN)
