import discord
import random
import asyncio
import os 
from message import send_embedded_warning, send_embedded_error,send_embedded_info
from feedback import get_active_threads, process_feedback
from dotenv import load_dotenv
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

last_warning = None
active_threads = []

# 權限設置
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents = intents)

async def update_active_threads():
    global active_threads
    active_threads = await get_active_threads()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    test_channel_id = 1199372364870340810  
    channel = client.get_channel(test_channel_id)
    client.loop.create_task(update_active_threads())
    if channel:
        await send_embedded_warning(channel)
        await asyncio.sleep(5)
        await send_embedded_error(channel)
        await asyncio.sleep(5)
        await send_embedded_info(channel)

# 監聽討論串訊息
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    for thread in active_threads:
        if message.channel.id == thread.id:
            await process_feedback(message, thread)
    

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