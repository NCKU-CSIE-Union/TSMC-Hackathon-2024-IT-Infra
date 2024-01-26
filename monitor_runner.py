import asyncio
import re
import threading
import time

import pandas as pd

from ai.analyze import analyze_by_llm
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


async def main():
    print("Running monitor runner...")
    logDF: pd.DataFrame = pd.DataFrame()
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    while True:
        for log_line in log.tail_log_entry(service_name="consumer-sentry"):
            parse_df = parser(log_line)
            logDF = pd.concat([logDF, parse_df], ignore_index=True)
            with open("log_data.csv", "w") as f:
                logDF.to_csv(f, index=False)
            result = analyze_by_llm(fill_missing_columns(logDF))
            asyncio.run_coroutine_threadsafe(
                broadcast(message_dict=result), client.loop
            )
        time.sleep(10)


asyncio.run(main())

# {
#     "discord_thread_1233": "uuid_4243343",
#     "uuid_4243343": "discord_thread_1233"
# }

# {
#     "123": {
#         "logs": List[pd.DataFrame],
#         "feedbacks": List[str],
#         "user_messages": List[str],
#     }
# }
