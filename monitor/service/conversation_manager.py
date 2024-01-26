# import asyncio
# import re

import pandas as pd

# from ai.analyze import analyze_by_llm
# from bot.bot import broadcast, client
# from monitor.service import cloudrun, log

import redis
import os
from dotenv import load_dotenv
import json
import ast
from functools import lru_cache


@lru_cache
def get_redis_setting():
    load_dotenv(".env/redis.env")
    return {
        "host": os.getenv("REDIS_HOST"),
        "port": os.getenv("REDIS_PORT"),
        "password": os.getenv("REDIS_PASSWORD"),
        "ssl": True,
        "decode_responses": True,
    }


class ConversationManager:
    def __init__(self):
        self.redis = redis.Redis(
            host="us1-wired-gar-38248.upstash.io",
            port=38248,
            password="521bab2680834c76b4ab8aface323626",
            ssl=True,
            decode_responses=True,
        )

    def new_conversation(self, discord_thread_id: str, log: pd.DataFrame):
        new_conversation = {
            "log": log.to_json(),
            "feedbacks": [],
            "user_messages": [],
        }

        for key in new_conversation:
            new_conversation[key] = str(json.dumps(new_conversation[key]))

        self.redis.hmset(discord_thread_id, new_conversation)

    def get_conversation(self, discord_thread_id: str) -> dict:
        """
        {
            "log": pd.DataFrame,
            "feedbacks": List[str],
            "user_messages": List[str],
        }
        """
        raw_json = self.redis.hgetall(discord_thread_id)
        raw_json["log"] = pd.read_json(json.loads(raw_json["log"]))
        raw_json["feedbacks"] = ast.literal_eval(raw_json["feedbacks"])
        raw_json["user_messages"] = ast.literal_eval(raw_json["user_messages"])

        return raw_json

    def update_conversation_feedbacks(self, discord_thread_id: str, feedbacks: str):
        """
        append the feedbacks to the feedbacks list
        """
        conversation_feedbacks = ast.literal_eval(
            self.redis.hget(discord_thread_id, "feedbacks")
        )

        conversation_feedbacks.append(feedbacks)
        self.redis.hset(discord_thread_id, "feedbacks", str(conversation_feedbacks))

    def update_conversation_user_messages(
        self, discord_thread_id: str, user_message: str
    ):
        conversation_user_messages = ast.literal_eval(
            self.redis.hget(discord_thread_id, "user_messages")
        )
        conversation_user_messages.append(user_message)
        self.redis.hset(
            discord_thread_id, "user_messages", str(conversation_user_messages)
        )


if __name__ == "__main__":
    manager = ConversationManager()

    df = pd.DataFrame()
    df["Time"] = [1, 2, 3, 4, 5]
    manager.new_conversation("discord_thread_1233", df)
    print(" create new conversation")

    print(manager.get_conversation("discord_thread_1233"))
    print(" get conversation")

    manager.update_conversation_feedbacks("discord_thread_1233", "feedback1")
    manager.update_conversation_feedbacks("discord_thread_1233", "feedback2")

    manager.update_conversation_user_messages("discord_thread_1233", "user_message1")
    print(" update conversation")

    print(manager.get_conversation("discord_thread_1233"))

    manager.update_conversation_feedbacks("discord_thread_1233", "feedback1")
    manager.update_conversation_feedbacks("discord_thread_1233", "feedback2")

    manager.update_conversation_user_messages("discord_thread_1233", "user_message1")
    print(" update conversation")

    print(manager.get_conversation("discord_thread_1233"))
