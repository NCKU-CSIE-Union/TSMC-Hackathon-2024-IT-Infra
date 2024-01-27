import os

import pandas as pd
import pytest
from dotenv import load_dotenv

from ai2.log_analyzer import LLMLogAnalyzer


@pytest.fixture(scope="class")
def llm_log_analyzer():
    load_dotenv()
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    llm_args = {
        "model_name": "text-bison@001",
        "max_output_tokens": 1024,
        "temperature": 0,
    }
    index_name = "tsmc-hackathon"
    return LLMLogAnalyzer(
        pinecone_api_key=pinecone_api_key, index_name=index_name, llm_args=llm_args
    )


@pytest.fixture(scope="class")
def log_data():
    return pd.read_csv("ai2/tests/data.csv").head(10)
