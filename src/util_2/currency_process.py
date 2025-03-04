
import requests
import json


# takes as argument list of new currencies
# gets currency code from list
# gets big dict from currency api
# uses code to access coresponding currency name from big dict of currencies
# stores id, code, and name in 3 variables 
# puts all three variables into dim table of dim_currency
# id is primary key
# ..... parquet

def currency_process(updated_rows: list):
    # currency_id = id from updated_rows
    # currency_code = code from updated rows
    # currency_dict = all currencies from api call
    # currency_name = currency_dict[currency_code]
    # 
    pass