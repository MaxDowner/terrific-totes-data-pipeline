from src.util_2.dim_date_to_parquet2 import create_dataset
import os
import pyarrow.parquet as pq

def test_create_dataset_returns_a_pq_file():
    if os.path.exists("/tmp/formatted_dim_date.parquet"):
        os.remove("/tmp/formatted_dim_date.parquet")
    create_dataset()
    assert os.path.exists("/tmp/formatted_dim_date.parquet")

def test_create_dataset_pq_file_is_readable():
    if os.path.exists("/tmp/formatted_dim_date.parquet"):
        os.remove("/tmp/formatted_dim_date.parquet")
    create_dataset()
    table = pq.read_table("/tmp/formatted_dim_date.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_date.parquet")
    assert str(table["year"][0]) == "2022"
    assert str(table["day_of_week"][0]) == '6'
    assert metadata.num_columns == 8
    assert metadata.num_rows == 3287
