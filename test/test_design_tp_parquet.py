import pandas as pd
from src.util_2.design_to_parquet import design_to_parquet



def test_():
    # Arrange
    updated_rows = [
    {"design_id": "data_1", "design_name": "data_2", "file_location": "data_3", "file_name" : "data_4"},
    {"design_id": "data_5", "design_name": "data_6", "file_location": "data_7", "file_name" : "data_8"},
    {"design_id": "data_9", "design_name": "data_10", "file_location": "data_11", "file_name" : "data_12"},
    ]
    # Act
    df = pd.read_parquet('test_results.parquet')
    df.to_json('check_json.json', orient='records')
    # Assert
    design_to_parquet(updated_rows)
    with open ('check_json.json', 'r') as f:
        body = f.read()

    print(body)
    assert False