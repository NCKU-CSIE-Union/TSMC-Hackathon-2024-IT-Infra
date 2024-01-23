import random
import time
import threading
import asyncio

from state.instance import Sleep, Counter, TotalQueryCount, AvgExecutionTime

from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks


def check_enque():
    return random.randint(0, 1)


def get_enque_num():
    return random.randint(1, 100)


def enqueue(num: int):
    Counter.increase(num)
    TotalQueryCount.increase(num)
    AvgExecutionTime.add_time(random.randint(1, 100), TotalQueryCount.get_count())


def mock_behavior():
    while True:
        if Sleep.check_sleep_time():
            sleep = Sleep.ack_sleep_time()
            print(f"sleep {sleep} seconds")
            time.sleep(sleep)
            continue

        if check_enque():
            current_enque_num = get_enque_num()
            print(f"enque {current_enque_num}")
            enqueue(current_enque_num)
            time.sleep(0.1)
        else:
            print("no consume")


@asynccontextmanager
async def backgound_mock_behavior(app: FastAPI, background_tasks: BackgroundTasks):
    print("start background task")
    background_tasks.add_task(mock_behavior)
    yield

    print("stop background task")


# never stop
async def background_task_exec(*args, **kwargs):
    while True:
        if Sleep.check_sleep_time():
            sleep = Sleep.ack_sleep_time()
            print(f"sleep {sleep} seconds")
            await asyncio.sleep(sleep)

        if check_enque():
            current_enque_num = get_enque_num()
            print(f"enque {current_enque_num}")
            enqueue(current_enque_num)
            await asyncio.sleep(0.1)
        else:
            print("no consume")


class BackgoundJobClass:
    def __init__(self, *args, **kwargs) -> None:
        self.task = asyncio.create_task(background_task_exec(*args, **kwargs))
