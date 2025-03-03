import os

from src.util_2.staff_to_parquet import process_staff

staff_dict = {
    "staff": [
      {
        "staff_id": 1,
        "first_name": "Jeremie",
        "last_name": "Franey",
        "department_name": "Purchasing",
        "location": "Manchester",
        "email_address": "jeremie.franey@terrifictotes.com"
      },
      {
        "staff_id": 2,
        "first_name": "Deron",
        "last_name": "Beier",
        "department_name": "Facilities",
        "location": "Manchester",
        "email_address": "deron.beier@terrifictotes.com"
      },
      {
        "staff_id": 3,
        "first_name": "Jeanette",
        "last_name": "Erdman",
        "department_name": "Facilities",
        "location": "Manchester",
        "email_address": "jeanette.erdman@terrifictotes.com"
      }
    ]
}

staff_list = staff_dict["staff"]

def test_process_staff_returns_a_pq_file():
    if os.path.exists("/tmp/formatted_dim_staff.parquet"):
        # print('file found')
        os.remove("/tmp/formatted_dim_staff.parquet")
    process_staff(staff_list)
    assert os.path.exists("/tmp/formatted_dim_staff.parquet")