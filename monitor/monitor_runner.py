import asyncio

import discord
import pandas as pd

from ai2.log_analyzer import LLMLogAnalyzer

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


class MonitorRunner:
    def __init__(
        self,
        llm_log_analyzer: LLMLogAnalyzer,
        client: discord.Client,
        channel_id: int,
        discord_thread_manager: DiscordThreadManager,
        target_service_name="consumer-latest",
        cloudrun_manager: CloudRunManager = CloudRunManager(),
    ):
        self.llm_log_analyzer = llm_log_analyzer
        self.discord_client = client
        self.channel_id = channel_id
        self.cloudrun_manager = cloudrun_manager
        self.discord_thread_manager = discord_thread_manager
        self.target_service_name = target_service_name

    def get_agent_response(self, conversion_id: str, user_message: str):
        return self.llm_log_analyzer.chat(conversion_id, user_message)

    async def send_alert(self, message_dict: dict):
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
        return thread.id

    def fetch_and_process_logs(self):
        log_df = pd.DataFrame()
        # Assume log.tail_log_entry is an async function
        for log_line in log.tail_log_entry(self.target_service_name, max_results=10):
            parse_df = parser(log_line)
            log_df = pd.concat([log_df, parse_df])
        return log_df

    def fetch_and_merge_metrics(self, log_df: pd.DataFrame):
        min_time = int(log_df["Time"].min().timestamp())
        max_time = int(log_df["Time"].max().timestamp())
        metrics_df = self.cloudrun_manager.get_metrics(
            self.target_service_name, min_time, max_time
        )
        metrics_df["Time"] = pd.to_datetime(metrics_df["Time"])
        log_df["Time"] = pd.to_datetime(log_df["Time"])
        merged_df = pd.merge(log_df, metrics_df, on="Time", how="inner")
        merged_df.sort_values("Time", inplace=True)
        return merged_df

    async def analyze_and_alert(self, merged_df: pd.DataFrame):
        """feed the merged dataframe to the log analyzer and send alert if needed

        Args:
            merged_df (pd.DataFrame): merged dataframe of log and metrics

        Returns:
            dict: keys: (['severity', 'cpu', 'memory', 'instance', 'message', 'prompt', 'metric_dataframe', 'timestamp'])
        """
        response = self.llm_log_analyzer.analyze_log(merged_df)
        if True:  # TODO: Replace with actual alert condition
            thread_id = asyncio.run_coroutine_threadsafe(
                self.send_alert(message_dict=response), self.discord_client.loop
            ).result()
            self.llm_log_analyzer.store_memory(
                id=str(thread_id),
                log_df=merged_df,
                initial_prompt=response["prompt"],
                response=response["message"],
            )
        return response

    async def update_service_configuration(self, response: dict):
        changed = False
        if response["instance"] != 0:
            changed = changed or await self.cloudrun_manager.increase_instance_count(
                self.target_service_name, response["instance"]
            )
        if response["cpu"] != 0 or response["memory"] != 0:
            changed = changed and await self.cloudrun_manager.increase_cpu_ram(
                self.target_service_name, response["cpu"], response["memory"]
            )
        if changed:
            service = await self.cloudrun_manager.get_service(self.target_service_name)
            print(
                "new resource configuration:",
                {
                    "cpu": service.template.containers[0].resources.limits["cpu"],
                    "memory": service.template.containers[0].resources.limits["memory"],
                    "instance": service.template.scaling.min_instance_count,
                },
            )

    async def periodic_monitor_task(self):
        print("fetching...")
        try:
            log_df = self.fetch_and_process_logs()
        except Exception as e:
            print("Error fetching logs:", e)
            return

        try:
            merged_df = self.fetch_and_merge_metrics(log_df)
        except Exception as e:
            print("Error fetching metrics:", e)
            return

        try:
            response = await self.analyze_and_alert(merged_df)
        except Exception as e:
            print("Error analyzing log:", e)
            return

        try:
            await self.update_service_configuration(response)
        except Exception as e:
            print("Error updating service configuration:", e)
            return

    async def run(self):
        while True:
            await self.periodic_monitor_task()
            await asyncio.sleep(60)
