from src.util.filepath_from_timestamp import filename_from_timestamp

class TestFilenameFromTimestampMethod:
    def test_returns_string_type(self):
        # Arrange
        input_timestamp = "1970-01-01 00:00:00.000"
        expected = str
        # Act
        result = filename_from_timestamp(input_timestamp)
        # Assert
        assert isinstance(result, expected)

    def test_returns_correct_year(self):
        # Arrange
        input_timestamp = "1992-11-16 17:45:11.848"
        expected = "1992"
        # Act
        result = filename_from_timestamp(input_timestamp)[1:5]
        # Assert
        assert expected == result

    def test_returns_correct_format(self):
        # Arrange
        input_timestamp = "1970-01-01 00:00:00.000"
        expected = "/1970/01/01/00/00-00"
        # Act
        result = filename_from_timestamp(input_timestamp)
        # Assert
        assert expected == result