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

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger("background")

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
