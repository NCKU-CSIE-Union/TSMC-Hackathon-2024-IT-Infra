import os
from functools import lru_cache


class Settings():
    full_cpu_process_count: int = os.getenv("FULL_CPU_PROCESS_COUNT", 4)
    full_ram_byte: int = os.getenv("FULL_RAM_BYTE", 1024*1024*1024*10)
    job_interval: int = os.getenv("JOB_INTERVAL", 1)
    enqueue_upper_bound: int = os.getenv("ENQUEUE_UPPER_BOUND", 100)
    enqueue_lower_bound: int = os.getenv("ENQUEUE_LOWER_BOUND", 1)
    dequeue_upper_bound: int = os.getenv("DEQUEUE_UPPER_BOUND", 100)
    dequeue_lower_bound: int = os.getenv("DEQUEUE_LOWER_BOUND", 1)
    execute_upper_bound: int = os.getenv("EXECUTE_UPPER_BOUND", 100)
    execute_lower_bound: int = os.getenv("EXECUTE_LOWER_BOUND", 10)


@lru_cache()
def get_settings():
    return Settings()