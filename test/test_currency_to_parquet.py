from src.util_2.currency_to_parquet import currency_to_parquet
import json 
import requests
import os

# test for 200 response code 

def test_currency_to_parquet_responds_with_a_200():
    # arrange
    input_data = [{'currency_id' : 1, 'currency_code' : 'USD'}]
    expected = 200
    # act
    result = currency_to_parquet(input_data)
    # assert
    assert result.status_code == expected
    converted_result = result.json()
    assert isinstance(converted_result, dict)

# test it's a json
# test it's a dictionary when converted to a python object


# test we're converting it to a jsonL?

# test file is created
# test it's a parquet file

def test_currency_to_parquet_returns_a_pq_file():
    # arrange
    if os.path.exists("/tmp/formatted_dim_currency.parquet"):
        os.remove("/tmp/formatted_dim_currency.parquet")
    input_data = [{'currency_id' : 1, 'currency_code' : 'USD'}]
    # act
    currency_to_parquet(input_data)
    # assert
    assert os.path.exists("/tmp/formatted_dim_currency.parquet")


# def test_pq_file_is_readable():
#     if os.path.exists("/tmp/formatted_dim_staff.parquet"):
#         os.remove("/tmp/formatted_dim_staff.parquet")
#     process_staff(staff_list)
#     # with open("/tmp/formatted_dim_staff.parquet", 'r') as f:
#     #     pass
#     table = pq.read_table("/tmp/formatted_dim_staff.parquet")
#     # parquet_file = pq.ParquetFile("/tmp/formatted_dim_staff.parquet")
#     metadata = pq.read_metadata("/tmp/formatted_dim_staff.parquet")
#     assert str(table["first_name"][0]) == "Jeremie"
#     assert str(table["department_name"][2]) == "Facilities"
#     assert metadata.num_columns == 6
#     assert metadata.num_rows == 3