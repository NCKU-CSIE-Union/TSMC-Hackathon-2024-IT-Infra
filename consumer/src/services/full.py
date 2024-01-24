import time
import multiprocessing
from core.config import get_settings

settings = get_settings()


def full_cpu_in_duration(duration: int):
    now = time.time()
    print("time", now)
    print(f"full cpu in {duration} seconds")

    n = settings.prime_upper_bound
    for num in range(2, n + 1):
        if time.time() > now + duration:
            break
        prime = True
        for i in range(2, num):
            if num % i == 0:
                prime = False
        if prime:
            pass

    print("time", time.time())


def create_full_cpu_process(duration: int):
    """
    create 4 process to full cpu in duration seconds
    """

    for _ in range(settings.full_cpu_process_count):
        p = multiprocessing.Process(target=full_cpu_in_duration, args=(duration,))
        p.start()


"""
refence: 
https://stackoverflow.com/questions/6317818/eat-memory-using-python
"""


def full_ram_in_duration(duration: int):
    now = time.time()
    print("time", now)
    print(f"full ram in {duration} seconds")

    cnt = 0
    a = bytearray(settings.full_ram_byte)
    while True:
        if time.time() > now + duration:
            break

        try:
            a = a + bytearray(settings.full_ram_byte)
            cnt += 1
        except MemoryError:
            break

    if time.time() < now + duration:
        time.sleep(now + duration - time.time())

    # in GB
    print(f"Allocated {cnt} GB in {duration} seconds")
    print("time", time.time())


def create_full_rem_process(duration: int):
    p = multiprocessing.Process(target=full_ram_in_duration, args=(duration,))
    p.start()
    return p
