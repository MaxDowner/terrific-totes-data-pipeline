from src.warehouse_lambda import warehouse_lambda_handler

def test_warehouse_lambda_gets_correct_bucket():
    # Arrange
    event = {
            'Records': [
                {'s3': 
                    {'bucket':
                        {'name': "processed-data"}
                    }
                }
            ]
    }
    expected = "processed-data"
    # Act
    result = warehouse_lambda_handler(event, {})
    # Assert
    assert expected == result