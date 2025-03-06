import logging
# import pg8000
import pandas as pd
import pyarrow
import pyarrow.dataset
import pyarrow.parquet as pq
import boto3
import adbc_driver_postgresql.dbapi as adbc
from src.util.get_secret import get_secret

table_list = ["currency",
              "staff",
              "design",
              "address",
              "counterparty",
              "sales_order"]
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
    uri = f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}"\
    f":{secret['port']}/{secret['dbname']}"
    print(uri) 

    conn = adbc.connect(uri)

    print(conn.adbc_get_table_schema(table_name)) 
    
    with conn.cursor() as cur:
        # reader = pq.ParquetFile(file)
        # print(reader)
        # cur.adbc_ingest(table_name, reader.iter_batches(), mode="create")

        # reader = pyarrow.dataset.dataset(

        # )
        table = pq.read_table(file)
        print(table)
        cur.adbc_ingest('fact_sales_order', table,mode='append')


if __name__ == '__main__':
    client = boto3.client("secretsmanager")
    db_details = get_secret(client, 'totes-data-warehouse')
    table = 'dim_staff'
    file = 'test_files/58-58formatted_fact_sales.parquet'
    load_to_dw(db_details, file, table)       
     



