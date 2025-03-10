import boto3
import pyarrow
import pyarrow.dataset
import pyarrow.parquet as pq
import adbc_driver_postgresql.dbapi as adbc
from src.util.get_secret import get_secret
import numpy as np

table_list = [
    "currency",
    "staff",
    "design",
    "address",
    "counterparty",
    "sales_order",
]
column_list = [
    ["currency_id", "currency_code"],
    [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ],
    ["design_id", "design_name", "file_location", "file_name"],
    [
        "address_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ],
    [
        "counterparty_id",
        "counterparty_legal_name",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ],
    [
        "sales_order_id",
        "staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_delivery_date",
        "agreed_payment_date",
        "agreed_delivery_location_id",
    ],
]

"""
Need to get the secret
"""
#  uri = "postgresql://postgres:password@localhost:5432/postgres"


def load_to_dw(secret, file, table_name):
    uri = (
        f"postgresql://{secret['username']}:"
        f"{secret['password']}@{secret['host']}"
        f":{secret['port']}/{secret['dbname']}"
    )
    # print(uri)

    conn = adbc.connect(uri)

    with conn.cursor() as cur:

        print(conn.adbc_get_table_schema("fact_sales_order"))

        table = pq.read_table(file)
        # print(table)
        panda_table = table.to_pandas()
        # print(panda_table)
        d = dict.fromkeys(
            panda_table.select_dtypes(np.int64).columns, np.int32
        )
        panda_table = panda_table.astype(d)
        # print(panda_table)

        arrow_table = pyarrow.Table.from_pandas(panda_table)
        print(arrow_table)
        result = cur.adbc_ingest(table_name, arrow_table, mode="append")
        print(result)

    conn.commit()


if __name__ == "__main__":
    client = boto3.client("secretsmanager")
    db_details = get_secret(client, "totes-data-warehouse")
    table_name = "fact_sales_order"
    file = "/tmp/formatted_fact_sales.parquet"
    load_to_dw(db_details, file, table_name)
