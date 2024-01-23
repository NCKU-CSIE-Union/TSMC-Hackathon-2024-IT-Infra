import os
from functools import lru_cache


class Settings:
    full_cpu_process_count: int = int(os.getenv("FULL_CPU_PROCESS_COUNT", 4))
    full_ram_byte: int = int(os.getenv("FULL_RAM_BYTE", 1024 * 1024 * 1024 * 10))
    job_interval: int = int(os.getenv("JOB_INTERVAL", 1))
    enqueue_upper_bound: int = int(os.getenv("ENQUEUE_UPPER_BOUND", 100))
    enqueue_lower_bound: int = int(os.getenv("ENQUEUE_LOWER_BOUND", 1))
    dequeue_upper_bound: int = int(os.getenv("DEQUEUE_UPPER_BOUND", 100))
    dequeue_lower_bound: int = int(os.getenv("DEQUEUE_LOWER_BOUND", 1))
    execute_upper_bound: int = int(os.getenv("EXECUTE_UPPER_BOUND", 100))
    execute_lower_bound: int = int(os.getenv("EXECUTE_LOWER_BOUND", 10))

    log_interval: int = int(os.getenv("LOG_INTERVAL", 1))
    log_file: str = os.getenv("LOG_FILE", "./log/consumer.log")
    log_max_bytes: int = int(os.getenv("LOG_MAX_BYTES", 10 * 1024 * 1024))  # 10MB
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", 10))  # 10 files


@lru_cache()
def get_settings():
    return Settings()
