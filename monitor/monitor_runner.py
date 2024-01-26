import asyncio
import time

import discord
import pandas as pd

# from bot.bot import cun_bot, send_alert
from bot.message import send_embedded_message
from bot.thread import DiscordThreadManager
from monitor.service import log
from monitor.service.cloudrun import CloudRunManager


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


class MonitorRunner:
    def __init__(
        self,
        chat_agent: FakeChatAI,
        client: discord.Client,
        channel_id: int,
        discord_thread_manager: DiscordThreadManager,
        target_service_name="consumer-latest",
        cloudrun_manager: CloudRunManager = CloudRunManager(),
    ):
        self.chat_agent = chat_agent
        self.discord_client = client
        self.channel_id = channel_id
        self.cloudrun_manager = cloudrun_manager
        self.discord_thread_manager = discord_thread_manager
        self.target_service_name = target_service_name

    def get_agent_response(self, conversion_id: str, user_message: str):
        return self.chat_agent.get_response(conversion_id, user_message)

    async def send_alert(self, message_dict: dict):
        print("broadcasting")
        test_channel_id = self.channel_id
        channel = self.discord_client.get_channel(test_channel_id)
        if channel:
            try:
                message = await send_embedded_message(channel, message_dict)
                return await self.create_thread(message)
            except Exception as e:
                print("Error sending warning message:", e)

    async def create_thread(self, message: discord.Message):
        thread: discord.Thread = await message.create_thread(name="Feedback Discussion")
        # 在討論串中發送一則 Welcome 訊息
        await thread.send("Send me message if you have any suggestion!")
        # 將討論串加入 active_threads 之中
        self.discord_thread_manager.add_thread(thread)
        # print(active_threads)
        return thread.id

    def run(self):
        # bot_thread = threading.Thread(target=run_bot)
        # bot_thread.start()
        while True:
            print("fetching...")

            log_df: pd.DataFrame = pd.DataFrame()
            for log_line in log.tail_log_entry(
                service_name=self.target_service_name, max_results=100
            ):
                parse_df = parser(log_line)
                log_df = pd.concat([log_df, parse_df])

            # get the min and max time
            min_time = int(log_df["Time"].min().timestamp())
            max_time = int(log_df["Time"].max().timestamp())

            metrics_df: pd.DataFrame = self.cloudrun_manager.get_metrics(
                self.target_service_name, min_time, max_time
            )
            metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
            log_df["Time"] = pd.to_datetime(log_df["Time"])
            merged_df = pd.merge(log_df, metrics_df, on="Time", how="inner")
            merged_df.sort_values("Time", inplace=True)

            # response = analyze_by_llm(merged_df)
            response = {  # TODO: substitute with analyze_by_llm
                "severity": "ERROR",
                "cpu": -1,
                "memory": 0,
                "instance": 1,
                "message": "The application is experiencing high latency and is unable to keep up with the demand. The number of tasks in the queue has been above 100 for the past 5 minutes and the average task execution time has been above 30 seconds. I recommend increasing the number of instances by 1.",
                "timestamp": "2024-01-26 11:05:49+00:00",
                # 'metric_dataframe': pd.DataFrame
            }

            # if response["need_alert"]:  # TODO: add alert condition
            thread_id = asyncio.run_coroutine_threadsafe(
                self.send_alert(message_dict=response), self.discord_client.loop
            ).result()

            print("new thread id created: ", thread_id)

            # if response["instance"] != 0:
            #     self.cloudrun_manager.increase_instance_count(
            #         self.target_service_name, response["instance"]
            #     )
            # if response["cpu"] != 0 or response["ram"] != 0:
            #     self.cloudrun_manager.increase_cpu_ram(
            #         self.target_service_name, response["cpu"], response["ram"]
            #     )
            time.sleep(60)
