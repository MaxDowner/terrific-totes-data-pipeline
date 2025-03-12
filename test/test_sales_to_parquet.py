import os
import pytest

from src.util_2.sales_to_parquet import sales_to_parquet
import pyarrow.parquet as pq


@pytest.fixture(autouse=True)
def sales():
    sales_list = [
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
                "agreed_delivery_location_id": 8,
                "created_date": "2022-11-03",
                "created_time": "14:20:52.186",
                "last_updated_date": "2022-11-04",
                "last_updated_time": "11:37:10.341"

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
                "agreed_delivery_location_id": 19,
                "created_date": "2022-11-03",
                "created_time": "14:20:52.186",
                "last_updated_date": "2022-11-04",
                "last_updated_time": "11:37:10.341"
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
                "agreed_delivery_location_id": 4,
                "created_date": "2022-11-03",
                "created_time": "14:20:52.186",
                "last_updated_date": "2022-11-04",
                "last_updated_time": "11:37:10.341"
            },
        ]

    return sales_list


def test_process_sales_returns_a_pq_file(sales):
    if os.path.exists("/tmp/formatted_fact_sales_order.parquet"):
        os.remove("/tmp/formatted_fact_sales_order.parquet")
    sales_to_parquet(sales)
    assert os.path.exists("/tmp/formatted_fact_sales_order.parquet")


def test_pq_file_is_readable(sales):
    if os.path.exists("/tmp/formatted_fact_sales_order.parquet"):
        os.remove("/tmp/formatted_fact_sales_order.parquet")
    sales_to_parquet(sales)
    table = pq.read_table("/tmp/formatted_fact_sales_order.parquet")
    metadata = pq.read_metadata("/tmp/formatted_fact_sales_order.parquet")
    assert str(table["units_sold"][2]) == "9000"
    assert str(table["currency_id"][1]) == "3"
    assert str(table['agreed_delivery_date'][1]) == "2022-11-06"
    assert metadata.num_columns == 14
    assert metadata.num_rows == 3
