import os
from src.util_2.address_to_parquet import address_to_parquet
import pyarrow.parquet as pq

address_dict = {
    "address": [
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
}

address_list = address_dict["address"]


def test_process_address_returns_a_pq_file():
    if os.path.exists("/tmp/formatted_dim_address.parquet"):
        os.remove("/tmp/formatted_dim_address.parquet")
    address_to_parquet(address_list)
    assert os.path.exists("/tmp/formatted_dim_address.parquet")


def test_pq_file_is_readable():
    if os.path.exists("/tmp/formatted_dim_address.parquet"):
        os.remove("/tmp/formatted_dim_address.parquet")
    address_to_parquet(address_list)
    # with open("/tmp/formatted_dim_address.parquet", 'r') as f:
    #     pass
    table = pq.read_table("/tmp/formatted_dim_address.parquet")
    # parquet_file = pq.ParquetFile("/tmp/formatted_dim_address.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_address.parquet")
    assert str(table["address_line_1"][0]) == "9 Bogart Hill"
    assert str(table["city"][2]) == "Morton"
    assert metadata.num_columns == 7
    assert metadata.num_rows == 3
