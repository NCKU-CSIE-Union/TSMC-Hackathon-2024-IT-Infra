import asyncio
import logging

from core.config import get_settings
from services.statistics import (
    get_cpu_percent,
    get_mem_usage,
    get_remain_count,
    get_avg_exe_time,
)


async def backgound_logging_task():
    """
    level,time,cpu,ram,remain_count,avg_exe_time
    """

    settings = get_settings()

    logging.basicConfig()
    logger = logging.getLogger("uvicorn.default")
    file_handler = logging.handlers.RotatingFileHandler(
        filename=settings.log_file,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s,%(message)s",
        datefmt="%H:%M:%S",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    while True:
        """
        level,time,cpu,ram,remain_count,avg_exe_time
        """
        logger.info(
            msg=f"{get_cpu_percent()},{get_mem_usage()},{get_remain_count()},{get_avg_exe_time()}"
        )
        # print("logging...")

        await asyncio.sleep(settings.log_interval)


class LoggingBackgroundClass:
    def __init__(self, *args, **kwargs) -> None:
        self.task = asyncio.create_task(backgound_logging_task(*args, **kwargs))
