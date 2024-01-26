import asyncio
import re

import pandas as pd

from ai.analyze import analyze_by_llm
from bot.bot import broadcast, client
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

    # bot_thread = threading.Thread(target=run_bot)
    # bot_thread.start()
    cloudrun_manager = cloudrun.CloudRunManager()

    while True:
        print("fetching...")
        log_df: pd.DataFrame = pd.DataFrame()
        for log_line in log.tail_log_entry(
            service_name="consumer-sentry", max_results=100
        ):
            parse_df = parser(log_line)
            log_df = pd.concat([log_df, parse_df], ignore_index=True)

        log_df["Time"] = log_df["time"]
        log_df = log_df.drop(columns=["time"])
        # convert `Time` column to datetime format eg. 2024-01-26 08:51:26
        log_df["Time"] = pd.to_datetime(log_df["Time"], format="%Y-%m-%d %H:%M:%S")
        # log_df = log_df.set_index("Time")

        # print(log_df)

        # get the min and max time
        min_time = int(log_df["Time"].min().timestamp())
        max_time = int(log_df["Time"].max().timestamp())
        # print(min_time, max_time, type(min_time), type(max_time))
        # TODO: convert the min and max time to the time.time() format

        metrics_df: pd.DataFrame = cloudrun_manager.get_metrics(
            "consumer-sentry", min_time, max_time
        )
        # print(metrics_df)
        # metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
        # log_df["Time"] = pd.to_datetime(log_df["Time"])

        log_df.to_csv("log.csv")
        metrics_df.to_csv("metrics.csv")
        print(metrics_df.columns, log_df.columns)
        metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
        log_df["Time"] = pd.to_datetime(log_df["Time"]).dt.floor("S")

        # Set a 60 seconds tolerance for merging
        tolerance = pd.Timedelta(seconds=60)

        # Perform an asof merge with a tolerance of 60 seconds
        merged_df = pd.merge_asof(
            metrics_df.sort_values("Time"),
            log_df.sort_values("Time"),
            on="Time",
            tolerance=tolerance,
            direction="nearest",
        )

        merged_df.to_csv("merge.csv")
        result = analyze_by_llm(fill_missing_columns(merged_df))
        manager = {}
        if result["need_report"]:
            thread_id = await asyncio.run_coroutine_threadsafe(
                broadcast(message_dict=result), client.loop
            ).result()
            manager.new_conversation(thread_id, merged_df)

        # pd.
        # result = analyze_by_llm(fill_missing_columns(merge_df))
        # asyncio.run_coroutine_threadsafe(
        #     broadcast(message_dict=result), client.loop
        # )

        # append to the csv file
        # with open("merge_data.csv", "a") as f:
        #     merge_df.to_csv(f, mode="a", header=f.tell() == 0)


asyncio.run(main())

# 1. Get the log from the cloud run
# 2. if ai say there is a problem, then send the message to the discord
# 3. before sending the message, generate a uuid for the thread
# {
#     "discord_thread_1233": {
#         "log": pd.DataFrame,
#         "feedbacks": List[str],
#         "user_messages": List[str],
#     }
# }

# manager (discord_thread_index, discord_conversation_store)

# manager.new_conversation(discord_thread_id: str, log: pd.DataFrame)
