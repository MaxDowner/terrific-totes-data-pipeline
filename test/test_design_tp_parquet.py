import pandas as pd
from src.util_2.design_to_parquet import design_to_parquet
import os

import pyarrow.parquet as pq


def test_design_to_parquet_returns_a_pq_file():
    # Arrange
    updated_rows = [{
                     "design_id": 1,
                     "design_name": "test_name",
                     "file_location": "test_location",
                     "file_name": "test_file_name"}]
    if os.path.exists("/tmp/formatted_dim_design.parquet"):
        os.remove("/tmp/formatted_dim_design.parquet")
    # Act
    design_to_parquet(updated_rows)
    # Assert
    assert os.path.exists("/tmp/formatted_dim_design.parquet")


def test_pq_file_is_readable():
    # Arrange
    updated_rows = [{"design_id": 1,
                     "design_name": "data_2",
                     "file_location": "data_3",
                     "file_name": "data_4"},
                    {"design_id": 5,
                     "design_name": "data_6",
                     "file_location": "data_7",
                     "file_name": "data_8"},
                    {"design_id": 9,
                     "design_name": "data_10",
                     "file_location": "data_11",
                     "file_name": "data_12"}]
    if os.path.exists("/tmp/formatted_dim_design.parquet"):
        os.remove("/tmp/formatted_dim_design.parquet")
    design_to_parquet(updated_rows)
    table = pq.read_table("/tmp/formatted_dim_design.parquet")
    metadata = pq.read_metadata("/tmp/formatted_dim_design.parquet")
    assert str(table['design_name'][0]) == 'data_2'
    assert str(table['file_location'][1]) == 'data_7'
    assert metadata.num_columns == 4
    assert metadata.num_rows == 3


def test_design_to_parquet_func_writes_a_datum_correctly():
    # Arrange
    json_check_file = 'tmp/dim_design_check_1.json'
    updated_rows = [{"design_id": 1,
                     "design_name": "test_name",
                     "file_location": "test_location",
                     "file_name": "test_file_name"}]
    expected = """[{"design_id":1,
                    "design_name":"test_name",
                    "file_location":"test_location",
                    "file_name":"test_file_name"}]"""
    # Act
    design_to_parquet(updated_rows)
    df = pd.read_parquet('/tmp/formatted_dim_design.parquet')
    df.to_json(json_check_file, orient='records')
    with open(json_check_file, 'r') as f:
        result = f.read()
    # Assert
    assert expected == result


def test_design_to_parquet_func_writes_multiple_data_correctly():
    # Arrange
    json_check_file = 'tmp/dim_design_check_1.json'
    updated_rows = [{"design_id": 1,
                     "design_name": "data_2",
                     "file_location": "data_3",
                     "file_name": "data_4"},
                    {"design_id": 5,
                     "design_name": "data_6",
                     "file_location": "data_7",
                     "file_name": "data_8"},
                    {"design_id": 9,
                     "design_name": "data_10",
                     "file_location": "data_11",
                     "file_name": "data_12"}]
    expected = """[{"design_id":1,
                    "design_name":"data_2",
                    "file_location":"data_3",
                    "file_name":"data_4"},
                   {"design_id":5,
                    "design_name":"data_6",
                    "file_location":"data_7",
                    "file_name":"data_8"},
                   {"design_id":9,
                    "design_name":"data_10",
                    "file_location":"data_11",
                    "file_name":"data_12"}]"""
    # Act
    design_to_parquet(updated_rows)
    df = pd.read_parquet('/tmp/formatted_dim_design.parquet')
    df.to_json(json_check_file, orient='records')
    with open(json_check_file, 'r') as f:
        result = f.read()
    # Assert
    assert expected == result
