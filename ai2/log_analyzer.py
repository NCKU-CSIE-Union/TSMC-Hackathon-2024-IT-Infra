import pandas as pd
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from pinecone import Pinecone
from vertexai.language_models import TextEmbeddingModel


class LLMLogAnalyzer:
    """
    LLMLogAnalyzer is a class that performs log analysis and provides scaling recommendations for a Google Cloud Run application.

    Args:
        pinecone_api_key (str): The API key for accessing the Pinecone service.
        index_name (str): The name of the Pinecone index.
        llm_args (dict): Additional arguments for initializing the VertexAI model.

    Attributes:
        llm (VertexAI): The VertexAI model for performing log analysis.
        db (Pinecone.Index): The Pinecone index for storing log embeddings.
        embedding_model (TextEmbeddingModel): The text embedding model for generating log embeddings.
        output_parser (StructuredOutputParser): The output parser for parsing the analysis feedback.
        format_instruction (str): The format instruction for providing scaling recommendations.
        prompt_template (PromptTemplate): The prompt template for generating analysis prompts.

    Methods:
        analyze_log: Analyzes the log data and provides scaling recommendations.
        store_memory: Stores the analysis feedback and log data in the Pinecone index.
        chat: Performs a conversation with the AI based on the stored analysis feedback.

    """

    def __init__(self, pinecone_api_key: str, index_name: str, llm_args: dict) -> None:
        """
        Initializes the LLMLogAnalyzer.

        Args:
            pinecone_api_key (str): The API key for accessing the Pinecone service.
            index_name (str): The name of the Pinecone index.
            llm_args (dict): Additional arguments for initializing the VertexAI model.
        """
        self.llm = VertexAI(**llm_args)

        pc = Pinecone(api_key=pinecone_api_key)
        self.db = pc.Index(index_name)

        self.embedding_model = TextEmbeddingModel.from_pretrained(
            "textembedding-gecko@003"
        )

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
        self.prompt_template = PromptTemplate.from_template(
            """\
The following text contains log data for a Google Cloud Run application. \
This data is presented in CSV format and encompasses the most recent {time_span} minutes:
{log_data}

{memory}

Some heuristic analysis has been performed beforehand, the following text is a summary of the analysis:
{heuristic_analysis}

Your task is to provide an in-depth analysis based on the provided log data and heuristic analysis feedback, \
and scale the application by providing the number of CPUs, amount of memory in MB, and amount of instances to add(positive) or remove(negative).
The system will automatically scale the application based on your feedback.

{format_instruction}
"""
        )

    def _heuristic_analysis(self, log_df: pd.DataFrame) -> str:
        """
        Performs heuristic analysis on the log data.

        Args:
            log_df (pd.DataFrame): The log data as a pandas DataFrame.

        Returns:
            str: The analysis feedback based on the heuristic analysis.
        """
        feedback = ""

        # Analyze CPU utilization
        cpu_label = "Container CPU Utilization (%)"
        for i in range(len(log_df) - 1):
            if log_df.iloc[i][cpu_label] > 40 and log_df.iloc[i + 1][cpu_label] > 40:
                feedback += f"- Container CPU Utilization (%) is above 40% for two minutes, at {log_df.iloc[i]['Time']} and {log_df.iloc[i + 1]['Time']}\n"

        # Analyze memory utilization
        mem_label = "Container Memory Utilization (%)"
        for i in range(len(log_df) - 1):
            if log_df.iloc[i][mem_label] > 50 and log_df.iloc[i + 1][mem_label] > 50:
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
        """
        Analyzes the log data with LLM and provides scaling recommendations.

        Args:
            log_df (pd.DataFrame): The log data as a pandas DataFrame.

        Returns:
            dict: A dictionary containing the analysis feedback and other information.
        """
        # Perform heuristic analysis to aid the model
        heuristic_feedback = self._heuristic_analysis(log_df)

        # Query a similar log from Pinecone, which acts as a memory for the model
        log_embedding = self.embedding_model.get_embeddings(
            [log_df.to_csv(index=False)]
        )[0].values
        matches = self.db.query(vector=log_embedding, top_k=1, include_metadata=True)[
            "matches"
        ]

        # Generate memory if a log with high similarity score is found in past analysis
        memory = ""
        if len(matches) > 0 and matches[0]["score"] > 0.8:
            similar_log = matches[0]
            memory = f"""\
We encountered a similar log in the past, with the following log data in CSV format:
{similar_log['metadata']['log_csv']}

The following text delimited by triple backticks is the chat history between a human and an AI, which is a summary of the analysis and scaling action taken in the past:
```
analysis: {similar_log['metadata']['chat_memory']}
```
"""

        # Define input variables for the prompt template
        input_variables = {
            "log_data": log_df.to_csv(index=False),
            "memory": memory,
            "time_span": len(log_df),
            "heuristic_analysis": heuristic_feedback,
            "format_instruction": self.format_instruction,
        }

        # Invoke the model
        prompt = self.prompt_template.format_prompt(**input_variables)
        feedback = self.llm.invoke(prompt)

        # Parse the output
        feedback_dict = self.output_parser.parse(feedback)

        # Add the prompt to the feedback, note that the prompt here does not include format instruction, to avoid unexpected response when chatting
        input_variables["format_instruction"] = ""
        feedback_dict["prompt"] = self.prompt_template.format_prompt(
            **input_variables
        ).text

        feedback_dict["metric_dataframe"] = log_df
        feedback_dict["timestamp"] = log_df.iloc[-1]["Time"]
        return feedback_dict

    def store_memory(
        self, id: str, log_df: pd.DataFrame, initial_prompt: str, response: str
    ):
        log_embedding = self.embedding_model.get_embeddings(
            [log_df.to_csv(index=False)]
        )[0].values

        # Manually format the memory as string because Pinecone does not support langchain memory as metadata
        # Note that the initial prompt is not included in the chat history, because we don't want to include it when
        # this information is retrieved for another analysis.
        chat_memory = f"AI: {response}"

        # Store the feedback in Pinecone
        self.db.upsert(
            vectors=[
                {
                    "id": id,
                    "values": log_embedding,
                    "metadata": {
                        "log_csv": log_df.to_csv(index=False),
                        "initial_prompt": initial_prompt,
                        "chat_memory": chat_memory,
                    },
                }
            ]
        )

    def chat(self, id: str, prompt: str) -> str:
        # Retrieve the memory from Pinecone
        record = self.db.fetch(ids=[id])["vectors"][id]
        initial_prompt = record["metadata"]["initial_prompt"]
        chat_memory = record["metadata"]["chat_memory"]

        # Generate response
        response = self.llm.invoke(
            f"""\
Prompt after formatting:
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. \
Please assume that the human is more experienced than the AI, and the AI should trust the human's judgement.

Current conversation:

Human: {initial_prompt}
{chat_memory}
Human: {prompt}
AI:

"""
        )

        # Update memory
        chat_memory += f"\nHuman: {prompt}\nAI: {response}\n"
        self.db.update(id=id, set_metadata={"chat_memory": chat_memory})

        return response
