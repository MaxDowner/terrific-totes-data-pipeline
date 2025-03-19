import os
import pytest
from src.util_2.counterparty_to_parquet import counterparty_to_parquet
import pyarrow.parquet as pq


@pytest.fixture(autouse=True)
def counterparty():
    counterparty_list = [
        {
            "counterparty_id": 1,
            "counterparty_legal_name": "Jeremie Ducket",
            "address_line_1": "12 Street Lane",
            "address_line_2": "Purchasing",
            "district": "Greater Manchester",
            "city": "Manchester",
            "postal_code": "M1 1AD",
            "country": "United Kingdom",
            "phone": "07284 611 038",
        },
        {
            "counterparty_id": 2,
            "counterparty_legal_name": "Susan Grey",
            "address_line_1": "12 Alaska Place",
            "address_line_2": None,
            "district": "Greatest Manchester",
            "city": "Salford",
            "postal_code": "M18 1BC",
            "country": "United Kingdom",
            "phone": "07984 892 729",
        },
        {
            "counterparty_id": 3,
            "counterparty_legal_name": "Pookie",
            "address_line_1": "9 Bogart Hill",
            "address_line_2": "Purchasing",
            "district": "Mid Manchester",
            "city": "Stockport",
            "postal_code": "SK39 7DG",
            "country": "United Kingdom",
            "phone": "07292 601 468",
        },
    ]
    return counterparty_list


def test_process_counterparty_returns_a_pq_file(counterparty):
    if os.path.exists("/tmp/formatted_dim_counterparty.parquet"):
        os.remove("/tmp/formatted_dim_counterparty.parquet")
    counterparty_to_parquet(counterparty)
    assert os.path.exists("/tmp/formatted_dim_counterparty.parquet")


def test_pq_file_is_readable(counterparty):
    if os.path.exists("/tmp/formatted_dim_counterparty.parquet"):
        os.remove("/tmp/formatted_dim_counterparty.parquet")
    counterparty_to_parquet(counterparty)
    table = pq.read_table("/tmp/formatted_dim_counterparty.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_counterparty.parquet")
    assert str(table["counterparty_legal_name"][0]) == "Jeremie Ducket"
    assert str(table["counterparty_legal_district"][2]) == "Mid Manchester"
    assert metadata.num_columns == 9
    assert metadata.num_rows == 3
