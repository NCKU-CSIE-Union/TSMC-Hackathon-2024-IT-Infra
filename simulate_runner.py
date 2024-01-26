import asyncio
import re
import threading
import time

import pandas as pd

from ai.analyze import analyze_by_llm
from ai.preprocess import preprocess_metric_data
from bot.bot import run_bot
from monitor.service import cloudrun

cloudrun.CloudRunManager()


def parser(line):
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}) (\w+): +(\d+\.\d+),(\d+\.\d+),(\d+),(\d+\.\d+)"

    match = re.match(pattern, line)
    if match:
        parsed_data = [match.groups()]

        df = pd.DataFrame(
            parsed_data,
            columns=["time", "level", "cpu", "ram", "remain_count", "avg_exe_time"],
        )

        df["time"] = pd.to_datetime(df["time"])
        df[["cpu", "ram", "avg_exe_time"]] = df[["cpu", "ram", "avg_exe_time"]].astype(
            float
        )
        df["remain_count"] = df["remain_count"].astype(int)

        return df


def fill_missing_columns(metric_df) -> pd.DataFrame:
    columns_to_fill = [
        "Instance Count (active)",
        "Instance Count (idle)",
        "Container CPU Utilization (%)",
        "Container Memory Utilization (%)",
        "Container Startup Latency (ms)",
        "Response Count (4xx)",
        "Response Count (5xx)",
    ]

    for column in columns_to_fill:
        if column not in metric_df.columns:
            metric_df[column] = 0

    metric_df["Time"] = metric_df["time"]

    return metric_df


class DataSimulator:
    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.current_index = 0

    def get_next_chunk(self, chunk_size: int = 10):
        # This method returns the next chunk of data
        start_index = self.current_index
        end_index = start_index + chunk_size
        if end_index > len(self.data):
            end_index = len(self.data)
        chunk = self.data[start_index:end_index]
        self.current_index = end_index
        return chunk

    def is_end(self):
        # This method checks if the end of the data is reached
        return self.current_index >= len(self.data)


async def main():
    simulate_data: pd.DataFrame = preprocess_metric_data("data/sample/")
    data_simulator = DataSimulator(simulate_data)
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    while not data_simulator.is_end():
        chunk = data_simulator.get_next_chunk(10)
        result = analyze_by_llm(chunk)
        print(result)
        # asyncio.run_coroutine_threadsafe(
        #         broadcast(message_dict=result), client.loop
        #     )
        time.sleep(6)


asyncio.run(main())
