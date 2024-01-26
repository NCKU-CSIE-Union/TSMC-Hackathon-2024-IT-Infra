# Global list to keep track of active threads
active_threads = []

async def get_active_threads():
    """
    Returns the list of active threads.
    """
    return active_threads

async def create_thread(message):
    """
    Creates a discussion thread for a given message and adds it to the active threads list.
    """
    # Create a discussion thread linked to the message
    thread = await message.create_thread(name="Feedback Discussion")
    # Send a welcome message in the newly created thread
    await thread.send("Send me message if you have any suggestion!")
    # Add the new thread to the list of active threads
    active_threads.append(thread)


def feedback_retrieval(message, thread_id):
    # TODO: Peter這邊 feedback_retrival(message, thread_id) 這裡面要做 store 的動作
    return "AI response"


async def process_feedback(message, thread):
    """
    Processes received feedback, sends a confirmation, and stores it.
    """
    ai_response = feedback_retrieval(message.content, thread.id)
    await thread.send(ai_response)
