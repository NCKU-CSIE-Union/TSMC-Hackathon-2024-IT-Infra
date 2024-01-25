import os

import pandas as pd


def preprocess_metric_data(data_dir: str) -> pd.DataFrame:
    metric_df = pd.DataFrame()
    for filename in os.listdir(data_dir):
        if metric_df.empty:
            metric_df = pd.read_csv(os.path.join(data_dir, filename))
        else:
            tmp_df = pd.read_csv(os.path.join(data_dir, filename))

            # Merge metric_df and tmp_df along the "Time" column
            metric_df = pd.merge(metric_df, tmp_df, on="Time", how="outer")

    return metric_df
