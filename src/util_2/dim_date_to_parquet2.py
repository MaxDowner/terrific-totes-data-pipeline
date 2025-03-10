import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np


def create_dataset():
    """
    returns a dataframe
    """
    # creates dataset
    df = pd.DataFrame({"date_id": pd.date_range("2022-01-01", "2030-12-31")})
    # df['date_id'] = df['date_id'].dt.date
    df["year"] = df.date_id.dt.year
    df["month"] = df.date_id.dt.month
    df["day"] = df.date_id.dt.day_of_year
    df["day_of_week"] = df.date_id.dt.weekday + 1
    df["day_name"] = df.date_id.dt.strftime("%A")
    df["month_name"] = df.date_id.dt.strftime("%B")
    df["quarter"] = df.date_id.dt.quarter
    df['date_id'] = df.date_id.dt.date

    print(df)
    # makes a file
    # table = pa.Table.from_pandas(df)
    # d = dict.fromkeys(df.select_dtypes(np.datetime64).columns, np.datetime64('2022-01-01','D'))
    # print(table)
    # pq.write_table(table, "/tmp/formatted_dim_date.parquet")
    df.to_parquet("/tmp/formatted_dim_date.parquet")

if __name__ == '__main__':
    create_dataset()