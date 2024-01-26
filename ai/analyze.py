import pandas as pd
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI


def analyze_cpu_usage(metric_df) -> str:
    feedback = ""
    label = "Container CPU Utilization (%)"
    for i in range(len(metric_df) - 1):
        curr_entry = metric_df.iloc[i][label]
        next_entry = metric_df.iloc[i + 1][label]
        if (
            not pd.isna(curr_entry)
            and not pd.isna(next_entry)
            and curr_entry > 60.0
            and next_entry > 60.0
        ):
            feedback += f"\
- ERROR: Container CPU Utilization (%) is above 60% for two minutes, at {metric_df.iloc[i]['Time']} and {metric_df.iloc[i + 1]['Time']}\n"

    if feedback == "":
        feedback = f"- INFO: Container CPU Utilization (%) is below 60% over the last {len(metric_df)} minutes.\n"

    return feedback


def analyze_mem_usage(metric_df) -> str:
    feedback = ""
    label = "Container Memory Utilization (%)"
    for i in range(len(metric_df) - 1):
        curr_entry = metric_df.iloc[i][label]
        next_entry = metric_df.iloc[i + 1][label]
        if (
            not pd.isna(curr_entry)
            and not pd.isna(next_entry)
            and curr_entry > 60.0
            and next_entry > 60.0
        ):
            feedback += f"\
- ERROR: Container Memory Utilization (%) is above 60% for two minutes, at {metric_df.iloc[i]['Time']} and {metric_df.iloc[i + 1]['Time']}\n"

    if feedback == "":
        feedback = f"- INFO: Container Memory Utilization (%) is below 60% over the last {len(metric_df)} minutes.\n"

    return feedback


def analyze_restart(metric_df) -> str:
    feedback = ""
    for _, row in metric_df.iterrows():
        if not pd.isna(row["Container Startup Latency (ms)"]):
            feedback += f"\
- ERROR: Cloud run restarted at {row['Time']}, with Container Startup Latency (ms) of {row['Container Startup Latency (ms)']} ms\n"

    if feedback == "":
        feedback = f"- INFO: Cloud run did not restart over the last {len(metric_df)} minutes.\n"

    return feedback


def analyze_instance_count(metric_df) -> str:
    feedback = ""
    for _, row in metric_df.iterrows():
        if pd.isna(row["Instance Count (active)"]):
            continue

        total_instance_count = (
            row["Instance Count (active)"] + row["Instance Count (idle)"]
        )
        if total_instance_count > 2:
            feedback += f"\
- ERROR: Total instance count is above 2 at {row['Time']}, with Instance Count (active) of {int(row['Instance Count (active)'])} and Instance Count (idle) of {int(row['Instance Count (idle)'])}\n"

    if feedback == "":
        feedback = f"- INFO: Total instance count is less than or equal to 2 over the last {len(metric_df)} minutes.\n"

    return feedback


def analyze_fail_response(metric_df: pd.DataFrame) -> str:
    feedback = ""
    failed_response_count = 0
    for _, row in metric_df.iterrows():
        if pd.isna(row["Request Count (4xx)"]):
            continue

        failed_response_count += row["Request Count (4xx)"]
        if row["Request Count (4xx)"] > 0:
            feedback += f"\
- ERROR: Failed response detected at {row['Time']}, with Request Count (4xx) of {int(row['Request Count (4xx)'])}\n"

    if failed_response_count == 0:
        feedback = f"- INFO: No failed response detected over the last {len(metric_df)} minutes.\n"
    else:
        feedback += f"- ERROR: Failed response detected {int(failed_response_count)} times over the last {len(metric_df)} minutes.\n"

    return feedback


def analyze_by_rule(metric_df: pd.DataFrame) -> str:
    feedback = ""
    feedback += analyze_cpu_usage(metric_df)
    feedback += analyze_mem_usage(metric_df)
    feedback += analyze_restart(metric_df)
    feedback += analyze_instance_count(metric_df)
    feedback += analyze_fail_response(metric_df)

    return feedback


def analyze_by_llm(metric_df: pd.DataFrame) -> dict:
    # Analysis feedback by heuristic rules
    heuristic_feedback = analyze_by_rule(metric_df)

    print(heuristic_feedback)
    print()

    # Define response schema
    severity_schema = ResponseSchema(
        name="severity",
        description='Severity level of the analysis feedback. \
Use "ERROR" if the analysis detects errors, "WARNING" for potential issues, or "INFO" if no problems are identified.',
    )
    message_schema = ResponseSchema(
        name="message",
        description="In-depth analysis feedback based on provided metrics(The description can span multiple lines and should be well formatted, use '\\n' to separate lines.)",
    )
    response_schema = [severity_schema, message_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instruction = output_parser.get_format_instructions()

    # Define the model and prompt template
    llm = VertexAI(
        model_name="text-bison@001",
        temperature=0.5,
        max_tokens=512,
        top_p=0.9,
        top_k=0,
    )
    prompt_template = PromptTemplate.from_template(
        """\
The following text contains metric data for a Google Cloud Run application. \
This data is presented in CSV format and encompasses the most recent {time_span} minutes:
{metric_data}

The following text is a heuristic analysis feedback of the metric data:
{heuristic_feedback}

The heuristic analysis feedback is based on the following rules:
- CPU limit > 60% (lasts 2 minutes)
- Memory limit > 60% (lasts 2 minutes)
- Cloud run re-start
- Instance count > 2
- Fail response (4xx, 5xx)

Provide a more in-depth analysis feedback based on the provided metric data and heuristic analysis feedback. \
The analysis should include the following information:
- Detailed summary of all the errors and potential problems.
- Potential cause of the error.
- Anticipate potential problems based on the metric data.
- Give suggestions on how to fix the error or potential problems.

{format_instruction}
"""
    )

    # Invoke the model
    chain = prompt_template | llm
    feedback = chain.invoke(
        {
            "time_span": len(metric_df),
            "metric_data": metric_df.to_string(),
            "heuristic_feedback": heuristic_feedback,
            "format_instruction": format_instruction,
        }
    )

    # Parse the feedback to a dictionary
    feedback_dict = output_parser.parse(feedback)
    return feedback_dict
