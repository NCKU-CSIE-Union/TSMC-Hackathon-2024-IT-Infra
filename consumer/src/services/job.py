import random
import asyncio

from core.config import get_settings
from state.instance import Sleep, Counter, TotalQueryCount, AvgExecutionTime

settings = get_settings()


def check_enque():
    return random.randint(0, 1)


def check_deque():
    return random.randint(0, 1)


def get_enque_num():
    return random.randint(settings.enqueue_lower_bound, settings.enqueue_upper_bound)


def get_deque_num():
    return random.randint(settings.dequeue_lower_bound, settings.dequeue_upper_bound)


def enqueue(num: int):
    Counter.increase(num)
    TotalQueryCount.increase(num)
    execution_time = random.randint(
        settings.execute_lower_bound, settings.execute_upper_bound
    )
    AvgExecutionTime.add_time(execution_time, TotalQueryCount.get_count())


def dequeue(num: int):
    Counter.decrease(num)


# never stop
async def mock_behavior_task(*args, **kwargs):
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
            print("no enque")

        if check_deque():
            current_deque_num = get_deque_num()
            remain = Counter.get_count()
            current_deque_num = min(current_deque_num, remain)

            print(f"deque {current_deque_num}")
            dequeue(current_deque_num)
            await asyncio.sleep(0.1)
        else:
            print("no deque")

        await asyncio.sleep(settings.job_interval)


class MockBehaviorBackgroundClass:
    def __init__(self, *args, **kwargs) -> None:
        self.task = asyncio.create_task(mock_behavior_task(*args, **kwargs))
