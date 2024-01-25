import threading

"""
- Counter
- Total Query Count
- Avg Execution Time
"""


class CounterModel:
    """
    remain query count
    """

    def __init__(self, count):
        self.count = count
        self.lock = threading.Lock()

    def get_count(self):
        with self.lock:
            return self.count

    def set_count(self, count):
        with self.lock:
            self.count = count

    def decrease(self, cnt: int):
        with self.lock:
            self.count -= cnt

    def increase(self, cnt: int):
        with self.lock:
            self.count += cnt


class TotalQueryCountModel:
    """
    total query count
    """

    def __init__(self, count):
        self.count = count
        self.lock = threading.Lock()

    def get_count(self):
        with self.lock:
            return self.count

    def set_count(self, count):
        with self.lock:
            self.count = count

    def increase(self, cnt: int):
        with self.lock:
            self.count += cnt


class AvgExecutionTimeModel:
    """
    average execution time
    """

    def __init__(self, avg_time):
        self.avg_time = avg_time
        self.lock = threading.Lock()

    def get_avg_time(self):
        with self.lock:
            return self.avg_time

    def set_avg_time(self, avg_time):
        with self.lock:
            self.avg_time = avg_time

    def add_time(self, time_add: float, last_cnt: float):
        """
        avg_time = (avg_time * cnt + time_add) / (cnt + 1)
        """
        with self.lock:
            self.avg_time = (self.avg_time * last_cnt + time_add) / (last_cnt + 1)


class SleepModel:
    """
    - set sleep time
    """

    def __init__(self, sleep_time):
        self.sleep_time = sleep_time
        self.lock = threading.Lock()

    def check_sleep_time(self) -> bool:
        with self.lock:
            return self.sleep_time > 0

    def ack_sleep_time(self):
        with self.lock:
            sleep = self.sleep_time
            self.sleep_time = 0
            return sleep

    def set_sleep_time(self, sleep_time):
        with self.lock:
            self.sleep_time = sleep_time


class BackgroudJobModel:
    def __init__(self):
        self.job_class_instance = None
        self.lock = threading.Lock()

    def set_instance(self, instance):
        with self.lock:
            self.job_class_instance = instance

    def get_instance(self):
        with self.lock:
            return self.job_class_instance
