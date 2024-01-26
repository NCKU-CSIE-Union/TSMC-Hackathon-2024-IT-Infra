import asyncio
import time

import pandas as pd

from monitor.service import cloudrun, conversation_manager, log


def parser(line: str):
    # pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}) (\w+): +(\d+\.\d+),(\d+\.\d+),(\d+),(\d+\.\d+)"
    # print(line)

    # match = re.match(pattern, line)
    # if match:
    # parsed_data = [match.groups()]
    parsed_data = [line.split(",")]

    parsed_data[0][0] += "+00:00"
    # print(parsed_data)

    df = pd.DataFrame(
        parsed_data,
        columns=[
            "Time",
            "cpu",
            "ram",
            "Remaining Task Count in Queue",
            "Average Task Execution Time",
        ],
    )

    df["Time"] = pd.to_datetime(df["Time"], utc=0)
    # add timezone utc=0 to the time column
    # df["Time"] = df["Time"].dt.tz_convert(tz="UTC")
    df.drop(columns=["cpu", "ram"], inplace=True)
    df = df.astype(
        {
            "Remaining Task Count in Queue": int,
            "Average Task Execution Time": float,
        }
    )

    return df


async def main():
    print("Running monitor runner...")

    # bot_thread = threading.Thread(target=run_bot)
    # bot_thread.start()
    conversation_manager.ConversationManager()
    cloudrun_manager = cloudrun.CloudRunManager()
    target_service_name = "consumer-latest"
    while True:
        print("fetching...")
        log_df: pd.DataFrame = pd.DataFrame()
        for log_line in log.tail_log_entry(
            service_name=target_service_name, max_results=100
        ):
            parse_df = parser(log_line)
            # print(parse_df)
            log_df = pd.concat([log_df, parse_df])

        # convert `Time` column to datetime format eg. 2024-01-26 08:51:26
        # log_df["Time"] = pd.to_datetime(log_df["Time"], format="%Y-%m-%d %H:%M:%S")
        # log_df = log_df.reset_index()

        # print(log_df)

        # get the min and max time
        min_time = int(log_df["Time"].min().timestamp())
        max_time = int(log_df["Time"].max().timestamp())
        # print(min_time, max_time, type(min_time), type(max_time))
        # TODO: convert the min and max time to the time.time() format

        metrics_df: pd.DataFrame = cloudrun_manager.get_metrics(
            target_service_name, min_time, max_time
        )
        print(metrics_df)
        # print(metrics_df)
        # print(metrics_df)
        # metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
        # log_df["Time"] = pd.to_datetime(log_df["Time"])

        # log_df.to_csv("log.csv")
        # metrics_df.to_csv("metrics.csv")
        # print(metrics_df.columns, log_df.columns)
        metrics_df["Time"] = (
            pd.to_datetime(metrics_df["Time"])
            # .dt.tz_convert("Asia/Taipei")
            # .tz_localize(None)
        )
        log_df["Time"] = (
            pd.to_datetime(log_df["Time"])
            # .dt.tz_convert("Asia/Taipei")
            # .tz_localize(None)
        )
        # log_df.drop(columns=["level"], inplace=True)
        # log_df.resample("1Min", on="Time").mean()

        # Set a 60 seconds tolerance for merging
        # tolerance = pd.Timedelta(seconds=60)

        # Perform an asof merge with a tolerance of 60 seconds
        # merged_df = pd.merge_asof(
        #     metrics_df.sort_values("Time"),
        #     log_df.sort_values("Time"),
        #     on="Time",
        #     tolerance=tolerance,
        #     direction="nearest",
        # )
        merged_df = pd.merge(log_df, metrics_df, on="Time", how="inner")
        merged_df.sort_values("Time", inplace=True)

        with open("merge.csv", "a") as f:
            merged_df.to_csv(f, mode="a", header=f.tell() == 0, index=False)
        time.sleep(60)
        # result = analyze_by_llm(fill_missing_columns(merged_df))

        # pd.
        # result = analyze_by_llm(fill_missing_columns(merge_df))
        # asyncio.run_coroutine_threadsafe(
        #     broadcast(message_dict=result), client.loop
        # )

        # append to the csv file
        # with open("merge_data.csv", "a") as f:
        #     merge_df.to_csv(f, mode="a", header=f.tell() == 0)


asyncio.run(main())

# {
#     "discord_thread_1233": "uuid_4243343",
#     "uuid_4243343": "discord_thread_1233"
# }

# {
#     "discord_thread_1233": {
#         "logs": List[pd.DataFrame],
#         "feedbacks": List[str],
#         "user_messages": List[str],
#     }
# }
