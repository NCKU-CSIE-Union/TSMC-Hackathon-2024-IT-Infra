import asyncio
import re
import threading
import time

import pandas as pd

from ai.analyze import (  # noqa: F401
    analyze_by_llm,
    analyze_cpu_usage,
    analyze_instance_count,
    analyze_mem_usage,
    analyze_restart,
)
from bot.bot import broadcast, client, run_bot
from monitor.service import cloudrun, log

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


async def main():
    print("Running monitor runner...")
    logDF: pd.DataFrame = pd.DataFrame()
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    # loop = asyncio.get_event_loop()
    # asyncio.run_coroutine_threadsafe(broadcast("hello"), loop)
    while True:
        for log_line in log.tail_log_entry(service_name="consumer-sentry"):
            # print(log)
            # print("separator")
            parse_df = parser(log_line)
            logDF = pd.concat([logDF, parse_df], ignore_index=True)
            with open("log_data.csv", "w") as f:
                logDF.to_csv(f, index=False)
            # result = analyze_by_llm(logDF) #TODO: fix: if key not exist, ignore that key
            result = {
                "severity": "WARNING",  # ERROR, WARNING or INFO
                "message": "Lets make love tonight",
            }
            print(result)
            asyncio.run_coroutine_threadsafe(
                broadcast(message_dict=result), client.loop
            )
            # await broadcast(result)
        # analyze_by_llm()
        time.sleep(10)


asyncio.run(main())
