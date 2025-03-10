from src.util_2.currency_to_parquet import currency_to_parquet

import os

import pyarrow.parquet as pq

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


def test_currency_to_parquet_returns_a_pq_file():
    # arrange
    if os.path.exists("/tmp/formatted_dim_currency.parquet"):
        os.remove("/tmp/formatted_dim_currency.parquet")
    input_data = [{"currency_id": 1, "currency_code": "USD"}]
    # act
    currency_to_parquet(input_data)
    # assert
    assert os.path.exists("/tmp/formatted_dim_currency.parquet")


def test_pq_file_is_readable():
    if os.path.exists("/tmp/formatted_dim_currency.parquet"):
        os.remove("/tmp/formatted_dim_currency.parquet")
    input_data = [{"currency_id": 1, "currency_code": "USD"}]
    currency_to_parquet(input_data)
    table = pq.read_table("/tmp/formatted_dim_currency.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_currency.parquet")
    assert str(table["currency_code"][0]) == "USD"
    assert str(table["currency_name"][0]) == "US Dollar"
    assert metadata.num_columns == 3
    assert metadata.num_rows == 1


def test_pq_can_process_input_lists_with_length_greater_than_1():
    if os.path.exists("/tmp/formatted_dim_currency.parquet"):
        os.remove("/tmp/formatted_dim_currency.parquet")
    input_data = [
        {"currency_id": 1, "currency_code": "GBP"},
        {"currency_id": 2, "currency_code": "USD"},
        {"currency_id": 3, "currency_code": "EUR"},
    ]
    currency_to_parquet(input_data)
    table = pq.read_table("/tmp/formatted_dim_currency.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_currency.parquet")
    assert str(table["currency_code"][2]) == "EUR"
    assert str(table["currency_name"][2]) == "Euro"
    assert metadata.num_columns == 3
    assert metadata.num_rows == 3
