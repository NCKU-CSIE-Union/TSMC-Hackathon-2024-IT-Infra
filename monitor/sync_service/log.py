import os
from dotenv import load_dotenv
from google.cloud import logging
from google.cloud.logging_v2 import LogEntry

load_dotenv(".env/dev.env")

project_id = "tsmccareerhack2024-icsd-grp5"
project_name = f"projects/{project_id}"
access_token = os.getenv("ACCESS_TOKEN")


# create credentials object
# https://googleapis.dev/python/google-auth/latest/reference/google.auth.credentials.html#google.auth.credentials.Credentials


def get_cloud_run_logs(service_name):
    client = logging.Client()
    logger = client.logger(service_name)
    logs = logger.list_entries()

    for log in logs:
        print(log.payload)


def get_all_avaliable_logs():
    # gcloud logging logs list

    # return
    # projects/[PROJECT_ID]/logs/[LOG_ID]
    # logger_name == logger_id
    pass


def list_all_log_entries():
    """
    logger_name == logger_id
    """
    # logger_name = "run.googleapis.com%2Fvarlog%2Fsystem"
    # logger_name = "projects/tsmccareerhack2024-icsd-grp5/logs/run.googleapis.com%2Fstdout"
    logger_name = (
        "projects/tsmccareerhack2024-icsd-grp5/logs/run.googleapis.com%2Fstderr"
    )

    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)

    print("Listing entries for logger {}:".format(logger.name))

    for entry in logger.list_entries():
        timestamp = entry.timestamp.isoformat()
        print("* {}: {}".format(timestamp, entry.payload))


def get_log_entry_cmd():
    # https://cloud.google.com/run/docs/logging#viewing-logs-gcloud
    # gcloud beta run services logs tail SERVICE --project PROJECT-ID
    # - SERVICE: The name of the Cloud Run service name
    # - PROJECT-ID: The project ID of the Cloud Run service

    # SERVICE : consumer-sentry
    # gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE" --project PROJECT-ID --limit 10
    # gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=consumer-sentry" --project tsmccareerhack2024-icsd-grp5 --limit 10
    pass


def get_log_entry_sdk():
    # https://cloud.google.com/run/docs/logging#viewing-logs-sdk
    #
    pass


def get_enque_deque_log():
    # resource.type="cloud_run_revision"
    # resource.labels.revision_name="consumer-sentry-00004-864"
    # resource.labels.service_name="consumer-sentry"
    # severity=DEFAULT
    # logName="projects/tsmccareerhack2024-icsd-grp5/logs/run.googleapis.com%2Fstdout"
    pass


def tail_log_entry():
    """
    resource.type="cloud_run_revision"
    resource.labels.revision_name="consumer-sentry-00004-864"
    resource.labels.service_name="consumer-sentry"
    severity=DEFAULT
    logName="projects/tsmccareerhack2024-icsd-grp5/logs/run.googleapis.com%2Fstderr"
    """

    client = logging.Client()
    logger_name = "run.googleapis.com%2Fstderr"
    logger = client.logger(logger_name)

    resource_type = '"cloud_run_revision"'
    revision_name = '"consumer-sentry-00004-864"'
    service_name = '"consumer-sentry"'
    severity = '"DEFAULT"'

    query: LogEntry = logger.list_entries(
        filter_=f"resource.type={resource_type} AND resource.labels.revision_name={revision_name} AND resource.labels.service_name={service_name} AND severity={severity}",
        max_results=10,
        order_by=logging.DESCENDING,
    )

    for entry in query:
        print(entry.payload)


# REST API
# https://cloud.google.com/logging/docs/reference/v2/rest
# https://cloud.google.com/logging/docs/reference/v2/rest#rest-resource:-v2.entries

if __name__ == "__main__":
    # get_cloud_run_logs("consumer-sentry")
    # list_all_log_entries()

    tail_log_entry()
