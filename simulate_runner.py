import asyncio
import threading
import time

import pandas as pd

from ai.analyze import analyze_by_llm
from ai.preprocess import preprocess_metric_data
from bot.bot import client, run_bot, send_alert
from monitor.service import cloudrun

cloudrun.CloudRunManager()


class RealTimeDataSimulator:
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
    data_simulator = RealTimeDataSimulator(simulate_data)
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    while not data_simulator.is_end():
        chunk = data_simulator.get_next_chunk(10)
        result = analyze_by_llm(chunk)
        print(result)
        asyncio.run_coroutine_threadsafe(send_alert(message_dict=result), client.loop)
        time.sleep(6)


asyncio.run(main())
