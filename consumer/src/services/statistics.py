import os
import psutil

from state.instance import Counter, AvgExecutionTime


def get_cpu_percent():
    # 1 second interval
    return psutil.cpu_percent(3)


def get_current_instance_count() -> int:
    return int(os.environ.get("INSTANCE_COUNT", 1))


def get_cpu_usage():
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15 / os.cpu_count()) * 100
    return cpu_usage / get_current_instance_count()


def get_mem_percent():
    return psutil.virtual_memory().percent / get_current_instance_count()


def get_mem_usage():
    """
    return memory usage in GB
    """
    return psutil.virtual_memory().used / ((1024.0**3) * get_current_instance_count())


def get_remain_count():
    return Counter.get_count()


def get_avg_exe_time():
    return AvgExecutionTime.get_avg_time()
