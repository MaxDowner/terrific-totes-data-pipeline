import os

from src.util_2.staff_to_parquet import process_staff
import pyarrow.parquet as pq

staff_dict = {
    "staff": [
        {
            "staff_id": 1,
            "first_name": "Jeremie",
            "last_name": "Franey",
            "department_name": "Purchasing",
            "location": "Manchester",
            "email_address": "jeremie.franey@terrifictotes.com",
        },
        {
            "staff_id": 2,
            "first_name": "Deron",
            "last_name": "Beier",
            "department_name": "Facilities",
            "location": "Manchester",
            "email_address": "deron.beier@terrifictotes.com",
        },
        {
            "staff_id": 3,
            "first_name": "Jeanette",
            "last_name": "Erdman",
            "department_name": "Facilities",
            "location": "Manchester",
            "email_address": "jeanette.erdman@terrifictotes.com",
        },
    ]
}

staff_list = staff_dict["staff"]


def test_process_staff_returns_a_pq_file():
    if os.path.exists("/tmp/formatted_dim_staff.parquet"):
        os.remove("/tmp/formatted_dim_staff.parquet")
    process_staff(staff_list)
    assert os.path.exists("/tmp/formatted_dim_staff.parquet")


def test_pq_file_is_readable():
    if os.path.exists("/tmp/formatted_dim_staff.parquet"):
        os.remove("/tmp/formatted_dim_staff.parquet")
    process_staff(staff_list)
    # with open("/tmp/formatted_dim_staff.parquet", 'r') as f:
    #     pass
    table = pq.read_table("/tmp/formatted_dim_staff.parquet")
    # parquet_file = pq.ParquetFile("/tmp/formatted_dim_staff.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_staff.parquet")
    assert str(table["first_name"][0]) == "Jeremie"
    assert str(table["department_name"][2]) == "Facilities"
    assert metadata.num_columns == 6
    assert metadata.num_rows == 3
