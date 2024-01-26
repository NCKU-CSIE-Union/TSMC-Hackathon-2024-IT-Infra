import asyncio
import threading
import time

import pandas as pd

from ai.analyze import analyze_by_llm
from bot.bot import run_bot
from monitor.service import cloudrun, conversation_manager, log


def parser(line: str):
    parsed_data = [line.split(",")]

    parsed_data[0][0] += "+00:00"

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


class FakeChatAI:
    # def __init__(self):
    # self.chatbot = conversation_manager.ConversationManager()
    def get_response(self, conversion_id: str, user_message: str):
        """_summary_

        Args:
            conversion_id (str): the id of the discord thread
            user_message (str): user's new input

        Returns:
            _type_: _description_
        """
        a = "fake response:" + user_message
        return a


async def main():
    print("Running monitor runner...")

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
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
            log_df = pd.concat([log_df, parse_df])

        # get the min and max time
        min_time = int(log_df["Time"].min().timestamp())
        max_time = int(log_df["Time"].max().timestamp())

        metrics_df: pd.DataFrame = cloudrun_manager.get_metrics(
            target_service_name, min_time, max_time
        )
        metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
        log_df["Time"] = pd.to_datetime(log_df["Time"])
        merged_df = pd.merge(log_df, metrics_df, on="Time", how="inner")
        merged_df.sort_values("Time", inplace=True)

        analyze_by_llm(merged_df)
        time.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())

# {
#     "discord_thread_1233": {
#         "logs": List[pd.DataFrame],
#         "feedbacks": List[str],
#         "user_messages": List[str],
#     }
# }
