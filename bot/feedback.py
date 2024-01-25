import discord

active_threads = []

async def get_active_threads():
    return active_threads  

async def send_feedback(content):
    # 看 Jerry 那邊要怎麼收
    pass

async def create_thread(message):
    # 創建討論串
    thread = await message.create_thread(name="Feedback Discussion")
    # 在討論串中發送一則 Welcome 訊息
    await thread.send("Send me message if you have any suggestion!")
    # 將討論串加入 active_threads 之中
    active_threads.append(thread)
    print(active_threads)


async def process_feedback(message, thread):
    await thread.send(f"This is your feedback\n {message.content}\n Thanks for your feedback, Jerry will take care of it!")
    print("成功發送「確認收到feedback訊息」")
    # await send_feedback(message)



    