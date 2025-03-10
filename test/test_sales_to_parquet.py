import os

from src.util_2.sales_to_parquet import sales_to_parquet
import pyarrow.parquet as pq

sales_dict = {
    "sales": [
            {
                "sales_order_id": 2,
                "created_date": 19,
                "created_time": 8,
                "last_updated_date": 42972,
                "last_updated_time": "3.94",
                "staff_id": 2,
                "counterparty_id": 3,
                "units_sold": "2022-11-07",
                "unit_price": "2022-11-08",
                "currency_id": 8,
                "design_id": "2022-11-03",
                "agreed_delivery_date": "14:20:52.186000",
                "agreed_payment_date": "2022-11-03",
                "agreed_delivery_location_id": "14:20:52.186000"
            },
            {
                "sales_order_id": 3,
                "created_date": 10,
                "created_time": 4,
                "last_updated_date": 65839,
                "last_updated_time": "2.91",
                "staff_id": 3,
                "counterparty_id": 4,
                "units_sold": "2022-11-06",
                "unit_price": "2022-11-07",
                "currency_id": 19,
                "design_id": "2022-11-03",
                "agreed_delivery_date": "14:20:52.188000",
                "agreed_payment_date": "2022-11-03",
                "agreed_delivery_location_id": "14:20:52.188000"
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
    table = pq.read_table("/tmp/formatted_fact_sales.parquet")
    metadata = pq.read_metadata("/tmp/formatted_fact_sales.parquet")
    assert str(table["units_sold"][1]) == "9000"
    assert str(table["currency_id"][1]) == "3"
    assert str(table['agreed_delivery_date'][1]) == "2022-11-06"
    assert metadata.num_columns == 14
    assert metadata.num_rows == 3
