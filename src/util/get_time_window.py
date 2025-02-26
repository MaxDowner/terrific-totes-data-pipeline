import csv
from datetime import datetime


def get_time_window():
    """Takes the current time and saves it to the log file.
    returns a tuple with the previous time run and the new time

    Returns:
        tuple: tuple with last time and current working time
    """

    time = datetime.now()

    with open('logs/last_run.csv', 'r+') as file:
        last_line = file.readlines()[-1]
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow([time, "None"])
    
    return (last_line.split(',')[0], str(time))