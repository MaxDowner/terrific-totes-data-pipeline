import boto3
import logging
import pyarrow
import pyarrow.dataset
import pyarrow.parquet as pq
import adbc_driver_postgresql.dbapi as adbc
from src.util.get_secret import get_secret
import numpy as np


logger = logging.getLogger("Load to warehouse logger")
logger.setLevel(logging.INFO)


def load_to_dw(secret, file, table_name):
    uri = (
        f"postgresql://{secret['username']}:"
        f"{secret['password']}@{secret['host']}"
        f":{secret['port']}/{secret['dbname']}"
    )

    conn = adbc.connect(uri)

    with conn.cursor() as cur:
        logger.info(f"Attempting to load file: {file}")
        # Code block converts file to pandas table and changes int type format
        table = pq.read_table(file)
        panda_table = table.to_pandas()
        d = dict.fromkeys(
            panda_table.select_dtypes(np.int64).columns, np.int32
        )
        panda_table = panda_table.astype(d)
        # Converts back to pyarrow table
        arrow_table = pyarrow.Table.from_pandas(panda_table)

        # fact_sales_order rows are not updated, only appended
        if table_name != "fact_sales_order":
            # Code block deletes rows with existing ids
            cur.execute(f"SELECT * FROM {table_name};")
            remote_table = cur.fetch_arrow_table()
            id_column = table_name[4:] + "_id"
            for id in arrow_table[id_column]:
                if id in remote_table[id_column]:
                    formatted_id = int(str(id))
                    cur.execute(f"DELETE FROM {table_name} WHERE {id_column} = {formatted_id};")

        result = cur.adbc_ingest(table_name, arrow_table, mode="append")

        logger.info(f"Adding/updating {result} entries to {table_name}")

    conn.commit()


if __name__ == "__main__":
    client = boto3.client("secretsmanager")
    db_details = get_secret(client, "totes-data-warehouse")
    table_name = "dim_staff"
    file = "/tmp/formatted_dim_staff.parquet"
    load_to_dw(db_details, file, table_name)
