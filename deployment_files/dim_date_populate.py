import boto3
import pyarrow
import adbc_driver_postgresql.dbapi as adbc
import pyarrow.parquet as pq
import numpy as np

from src.util.get_secret import get_secret
from src.util_2.dim_date_to_parquet2 import create_dataset


def dim_date_populate():
    """Only neewd to run the first time
    Connects to the database and populates the date table if needed
    """
    # connect to db using arrow
    # check for data
    # if none run the file
    #  populate
    client = boto3.client("secretsmanager")
    secret = get_secret(client, "totes-data-warehouse")
    table_name = "dim_date"
    file = "/tmp/formatted_dim_date.parquet"
    uri = (
        f"postgresql://{secret['username']}:"
        f"{secret['password']}@{secret['host']}"
        f":{secret['port']}/{secret['dbname']}"
    )

    conn = adbc.connect(uri)

    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table_name};")
        remote_date_table = cur.fetch_arrow_table()
        print(len(remote_date_table["year"]))
        if len(remote_date_table["year"]) > 0:
            create_dataset()
            table = pq.read_table(file)
            panda_table = table.to_pandas()
            d = dict.fromkeys(
                panda_table.select_dtypes(np.int64).columns, np.int32
            )
            panda_table = panda_table.astype(d)
            arrow_table = pyarrow.Table.from_pandas(panda_table)
            result = cur.adbc_ingest(table_name, arrow_table, mode="append")
            print(result)
            conn.commit()


if __name__ == "__main__":
    dim_date_populate()
