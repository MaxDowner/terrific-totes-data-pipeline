import os
from src.util_2.address_to_parquet import address_to_parquet
import pytest
import pyarrow.parquet as pq


@pytest.fixture(autouse=True)
def address():

    address_list = [
        {
            "address_id": 1,
            "address_line_1": "9 Bogart Hill",
            "address_line_2": "Avon",
            "district": "Avon",
            "city": "Patienceburgh",
            "postal_code": "WM60 3FH",
            "country": "Turkey",
        },
        {
            "address_id": 2,
            "address_line_1": "12 Street Lane",
            "address_line_2": None,
            "district": "Aliso Viejo",
            "city": "Aliso Viejo",
            "postal_code": "ED6 12PY",
            "country": "San Marino",
        },
        {
            "address_id": 30,
            "address_line_1": "12 Alaska Place",
            "address_line_2": "The Avenue",
            "district": "Buckinghamshire",
            "city": "Morton",
            "postal_code": "NG9 8IP",
            "country": "Falkland Islands (Malvinas)"
        }
    ]
    return address_list


def test_process_address_returns_a_pq_file(address):
    if os.path.exists("/tmp/formatted_dim_location.parquet"):
        os.remove("/tmp/formatted_dim_location.parquet")
    address_to_parquet(address)
    assert os.path.exists("/tmp/formatted_dim_location.parquet")


def test_pq_file_is_readable(address):
    if os.path.exists("/tmp/formatted_dim_location.parquet"):
        os.remove("/tmp/formatted_dim_location.parquet")
    address_to_parquet(address)
    table = pq.read_table("/tmp/formatted_dim_location.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_location.parquet")
    assert str(table["address_line_1"][0]) == "9 Bogart Hill"
    assert str(table["city"][2]) == "Morton"
    assert metadata.num_columns == 7
    assert metadata.num_rows == 3
