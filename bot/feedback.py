active_threads = []


async def get_active_threads():
    return active_threads


async def create_thread(message):
    # 創建討論串
    thread = await message.create_thread(name="Feedback Discussion")
    # 在討論串中發送一則 Welcome 訊息
    await thread.send("Send me message if you have any suggestion!")
    # 將討論串加入 active_threads 之中
    active_threads.append(thread)
    print(active_threads)


async def process_feedback(message, thread):
    print(f"收到feedback:{message.content}")
    await thread.send(
        "Feedback received ! Thanks for your feedback, we will use this to improve our message!"
    )
    print(message.content)
    print(thread.id)
    # Peter這邊 feedback_retrival(message.content, thread.id)
