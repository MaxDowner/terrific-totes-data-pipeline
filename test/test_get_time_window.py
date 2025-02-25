import csv
import os
from datetime import datetime

from src.util.get_time_window import get_time_window

# Test the returns
def test_returns_tuple():
    result = get_time_window()
    assert isinstance(result, tuple)

def test_tuple_returns_2_strings():
    result = get_time_window()
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)

def test_returns_valid_datetime_format():
    result = get_time_window()
    format = '%Y-%m-%d %H:%M:%S.%f'
    date_1_formatted = datetime.strptime(result[0], format)
    date_2_formatted = datetime.strptime(result[1], format)
    assert result[0] == str(date_1_formatted)
    assert result[1] == str(date_2_formatted)

# test the csv

def test_writes_to_csv():
    with open('logs/last_run.csv', 'r') as file:
        lines_before = len(file.readlines())
    with open('logs/last_run.csv', "rb") as file:
    # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_before = file.readline().decode()
    get_time_window()
    with open('logs/last_run.csv', 'r') as file:
        lines_after = len(file.readlines())
        # updated_last_line = file.readlines()[-1]
    with open('logs/last_run.csv', "rb") as file:
    # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_after = file.readline().decode()
    assert last_line_before != last_line_after
    assert lines_after == lines_before + 1

def test_adds_time_and_None():
    result = get_time_window()
    with open('logs/last_run.csv', "rb") as file:
    # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line = file.readline().decode()
    items = last_line.split(',')
    assert items[0] == result[1]
    assert items[1].strip() == 'None'