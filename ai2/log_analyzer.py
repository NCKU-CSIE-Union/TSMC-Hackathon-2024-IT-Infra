import pandas as pd
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from pinecone import Pinecone


class LLMLogAnalyzer:
    def __init__(self, pinecone_api_key: str, index_name: str, llm_args: dict) -> None:
        self.llm = VertexAI(**llm_args)

        pc = Pinecone(api_key=pinecone_api_key)
        self.db = pc.Index(index_name)

        # Define output parser and generate format instruction
        severity_schema = ResponseSchema(
            name="severity",
            description='The severity of the analysis feedback is categorized as follows: "ERROR" indicates severe problems that require immediate scaling action, "WARNING" suggests less severe issues that nonetheless require caution, and "INFO" denotes the absence of problems.',
        )
        cpu_schema = ResponseSchema(
            name="cpu",
            description="Number of CPUs to add(positive) or remove(negative) to each instance.",
            type="int",
        )
        mem_schema = ResponseSchema(
            name="memory",
            description="Amount of memory in MB to add(positive) or remove(negative) to each instance.",
            type="int",
        )
        instance_schema = ResponseSchema(
            name="instance",
            description="Amount of instances to add(positive) or remove(negative).",
            type="int",
        )
        message_schema = ResponseSchema(
            name="message",
            description="In-depth and well formatted analysis in markdown format.",
        )
        self.output_parser = StructuredOutputParser.from_response_schemas(
            [severity_schema, cpu_schema, mem_schema, instance_schema, message_schema]
        )
        self.format_instruction = self.output_parser.get_format_instructions()

        # Define model and prompt template
        prompt_template = PromptTemplate.from_template(
            """\
The following text contains log data for a Google Cloud Run application. \
This data is presented in CSV format and encompasses the most recent {time_span} minutes:
{log_data}

Some heuristic analysis has been performed beforehand, the following text is a summary of the analysis:
{heuristic_analysis}

Your task is to provide an in-depth analysis based on the provided log data and heuristic analysis feedback, \
and scale the application by providing the number of CPUs, amount of memory in MB, and amount of instances to add(positive) or remove(negative).
The system will automatically scale the application based on your feedback.

{format_instruction}
"""
        )

        # Define analysis chain
        self.analysis_chain = prompt_template | self.llm

    def _heuristic_analysis(self, log_df: pd.DataFrame) -> str:
        feedback = ""

        # Analyze CPU utilization
        cpu_label = "Container CPU Utilization (%)"
        for i in range(len(log_df) - 1):
            if log_df.iloc[i][cpu_label] > 40 and log_df.iloc[i + 1][cpu_label] > 40:
                feedback += f"- Container CPU Utilization (%) is above 40% for two minutes, at {log_df.iloc[i]['Time']} and {log_df.iloc[i + 1]['Time']}\n"

            # Analyze memory utilization
            mem_label = "Container Memory Utilization (%)"
            for i in range(len(log_df) - 1):
                if (
                    log_df.iloc[i][mem_label] > 50
                    and log_df.iloc[i + 1][mem_label] > 50
                ):
                    feedback += f"- Container Memory Utilization (%) is above 50% for two minutes, at {log_df.iloc[i]['Time']} and {log_df.iloc[i + 1]['Time']}\n"

            # Analyze remaining task count in queue
            for i in range(len(log_df)):
                if log_df.iloc[i]["Remaining Task Count in Queue"] > 100:
                    feedback += f"- Remaining Task Count in Queue is above 100 at {log_df.iloc[i]['Time']}\n"

            # Analyze average task execution time
            for i in range(len(log_df)):
                if log_df.iloc[i]["Average Task Execution Time"] > 30:
                    feedback += f"- Average Task Execution Time is above 30 seconds at {log_df.iloc[i]['Time']}\n"

            return feedback

    def analyze_log(self, log_df: pd.DataFrame) -> dict:
        # Perform heuristic analysis to aid the model
        heuristic_feedback = self._heuristic_analysis(log_df)

        # Invoke the model
        feedback = self.analysis_chain.invoke(
            {
                "log_data": log_df.to_csv(index=False),
                "time_span": len(log_df),
                "heuristic_analysis": heuristic_feedback,
                "format_instruction": self.format_instruction,
            }
        )

        # Parse the output
        feedback_dict = self.output_parser.parse(feedback)
        feedback_dict["metric_dataframe"] = log_df
        feedback_dict["timestamp"] = log_df.iloc[-1]["Time"]
        return feedback_dict
