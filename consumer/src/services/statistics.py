import os
import psutil

from state.instance import Counter, AvgExecutionTime


def get_cpu_percent():
    # 1 second interval
    return psutil.cpu_percent(1)


def get_cpu_usage():
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15 / os.cpu_count()) * 100
    return cpu_usage


def get_mem_percent():
    return psutil.virtual_memory().percent


def get_mem_usage():
    """
    return memory usage in GB
    """
    return psutil.virtual_memory().used / (1024.0**3)


def get_remain_count():
    return Counter.get_count()


def get_avg_exe_time():
    return AvgExecutionTime.get_avg_time()
