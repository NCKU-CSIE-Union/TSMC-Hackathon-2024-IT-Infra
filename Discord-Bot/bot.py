import discord
import random
import asyncio
import os

last_warning = None

# 權限設置
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents = intents)
    
# 測試 function
async def pull_warning():
    num = random.randint(0,100)
    return f"編號{num}這是一個新的警告！"

async def warning_task():
    global last_warning
    while True:
        # 呼叫 pull_warning 函數獲取最新警告
        new_warning = await pull_warning()
        if new_warning != last_warning:
            # 如果新警告與上一次警告不同，則向 Discord 頻道發送新警告
            last_warning = new_warning
            channel = client.get_channel(1199372364870340810)  
            await channel.send(new_warning)
        await asyncio.sleep(5)  


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print("TSMC System Bot is Online!")
    client.loop.create_task(warning_task())

    
client.run("MTE5OTI3MTYxMzM1OTczOTAxMA.GJN31L.rNSDr17bJ4cMPOsKeLd4jFdS45wZqVGcrDmo6k")