import os

from src.util_2.sales_to_parquet import sales_to_parquet
import pyarrow.parquet as pq

sales_dict = {
    "sales": [
        {
            "sales_order_id": 2,
            "staff_id": 1,
            "counterparty_id": 1,
            "units_sold": 500,
            "unit_price": "3.94",
            "currency_id": 2,
            "design_id": 3,
            "agreed_delivery_date": "2022-11-07",
            "agreed_payment_date": "2022-11-08",
            "agreed_delivery_location_id": 8
        },
        {
            "sales_order_id": 3,
            "staff_id": 2,
            "counterparty_id": 2,
            "units_sold": 600,
            "unit_price": "2.91",
            "currency_id": 3,
            "design_id": 4,
            "agreed_delivery_date": "2022-11-06",
            "agreed_payment_date": "2022-11-07",
            "agreed_delivery_location_id": 19
        },
        {
            "sales_order_id": 30,
            "staff_id": 3,
            "counterparty_id": 20,
            "units_sold": 9000,
            "unit_price": "3.99",
            "currency_id": 3,
            "design_id": 2,
            "agreed_delivery_date": "2022-11-26",
            "agreed_payment_date": "2022-11-28",
            "agreed_delivery_location_id": 4
        },
    ]
}

sales_list = sales_dict["sales"]


def test_process_sales_returns_a_pq_file():
    if os.path.exists("/tmp/formatted_fact_sales.parquet"):
        os.remove("/tmp/formatted_fact_sales.parquet")
    sales_to_parquet(sales_list)
    assert os.path.exists("/tmp/formatted_fact_sales.parquet")


def test_pq_file_is_readable():
    if os.path.exists("/tmp/formatted_fact_sales.parquet"):
        os.remove("/tmp/formatted_fact_sales.parquet")
    sales_to_parquet(sales_list)
    # with open("/tmp/formatted_fact_sales.parquet", 'r') as f:
    #     pass
    table = pq.read_table("/tmp/formatted_fact_sales.parquet")
    # parquet_file = pq.ParquetFile("/tmp/formatted_fact_sales.parquet")
    metadata = pq.read_metadata("/tmp/formatted_fact_sales.parquet")
    assert str(table["units_sold"][2]) == "9000"
    assert str(table["currency_id"][1]) == "3"
    assert metadata.num_columns == 9
    assert metadata.num_rows == 3
