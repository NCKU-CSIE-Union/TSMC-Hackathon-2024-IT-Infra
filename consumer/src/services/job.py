import random
import asyncio
import os
import time
from multiprocessing import Process

from core.config import get_settings
from state.instance import Sleep, Counter, TotalQueryCount, AvgExecutionTime

settings = get_settings()


def get_current_instance_count() -> int:
    return int(os.environ.get("INSTANCE_COUNT", 1))


def fake_job(pid: int):
    """
    calculate prime number
    """
    print(f"start job {pid}")

    n = int(random.uniform(settings.prime_lower_bound, settings.prime_upper_bound))
    print(f"prime {n}")

    for num in range(2, n + 1):
        prime = True
        for i in range(2, num):
            if num % i == 0:
                prime = False
        if prime:
            pass

    # remove pid file
    os.remove(f"./{pid}.pid")


def check_enque():
    return random.randint(0, 1)


def check_deque():
    return random.randint(0, 1)


def get_enque_num():
    return random.randint(settings.enqueue_lower_bound, settings.enqueue_upper_bound)


def enqueue(num: int):
    Counter.increase(num)


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
        else:
            print("no enque")

        remain = Counter.get_count()
        if remain > 0:
            Counter.decrease(1)
            now = time.time()

            # write pid file
            pid = random.randint(1, 100000)
            with open(f"./{pid}.pid", "w") as f:
                f.write(str(pid))

            p = Process(target=fake_job, args=(pid,))
            p.start()

            # block until job done
            while True:
                if not os.path.exists(f"./{pid}.pid"):
                    break
                await asyncio.sleep(0.5)

            execution_time = time.time() - now
            print(f"dequeue 1, execution time: {execution_time}")
            AvgExecutionTime.add_time(execution_time, TotalQueryCount.get_count())
            TotalQueryCount.increase(1)


class MockBehaviorBackgroundClass:
    def __init__(self, *args, **kwargs) -> None:
        self.task = asyncio.create_task(mock_behavior_task(*args, **kwargs))
