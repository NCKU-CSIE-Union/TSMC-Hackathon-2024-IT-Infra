import os

import pandas as pd


def preprocess_official_log_data(data_dir: str) -> pd.DataFrame:
    log_df = pd.DataFrame()
    for filename in os.listdir(data_dir):
        # Skip the container startup latency file
        if filename == "Container Startup Latency.csv":
            continue

        if log_df.empty:
            log_df = pd.read_csv(os.path.join(data_dir, filename))
        else:
            tmp_df = pd.read_csv(os.path.join(data_dir, filename))

            # Merge log_df and tmp_df along the "Time" column
            log_df = pd.merge(log_df, tmp_df, on="Time")

    return log_df
