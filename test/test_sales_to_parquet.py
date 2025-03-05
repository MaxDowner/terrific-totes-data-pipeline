import os

from src.util_2.sales_to_parquet import sales_to_parquet
import pyarrow.parquet as pq

sales_dict = {
    "sales": [
        {
            "sales_id": 1,
            "sales_legal_name": "Jeremie Ducket",
            "address_line_1": "12 Street Lane",
            "address_line_2": "Purchasing",
            "district": "Greater Manchester",
            "city": "Manchester",
            "postal_code": "M1 1AD",
            "country": "United Kingdom",
            "phone": "07284 611 038",
        },
        {
            "sales_id": 2,
            "sales_legal_name": "Susan Grey",
            "address_line_1": "12 Alaska Place",
            "address_line_2": None,
            "district": "Greatest Manchester",
            "city": "Salford",
            "postal_code": "M18 1BC",
            "country": "United Kingdom",
            "phone": "07984 892 729",
        },
        {
            "sales_id": 3,
            "sales_legal_name": "Pookie",
            "address_line_1": "9 Bogart Hill",
            "address_line_2": "Purchasing",
            "district": "Mid Manchester",
            "city": "Stockport",
            "postal_code": "SK39 7DG",
            "country": "United Kingdom",
            "phone": "07292 601 468",
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
    assert str(table["sales_legal_name"][0]) == "Jeremie Ducket"
    assert str(table["district"][2]) == "Mid Manchester"
    assert metadata.num_columns == 9
    assert metadata.num_rows == 3
