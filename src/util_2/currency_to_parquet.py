import requests
import json
from pyarrow import json as pj
import pyarrow.parquet as pq


# takes as argument list of new currencies
# gets currency code from list
# gets big dict from currency api
# uses code to access coresponding currency name from big dict of currencies
# stores id, code, and name in 3 variables 
# puts all three variables into dim table of dim_currency
# id is primary key
# ..... parquet

def currency_to_parquet(updated_rows: list):
    ''''''
    # make api call and save to response
    url = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json'
    response = requests.get(url)
    print(response)
    object_response = response.json()
    # add currency name to dict for all currencies
    for dict in updated_rows:
        currency_code = dict['currency_code'].lower()
        currency_name = object_response[currency_code]
        dict['currency_name'] = currency_name
    print(updated_rows)

    # convert to json lines
    with open('/tmp/output_currency_dict.json', 'w') as file:
        for dictionary in updated_rows:
            line = json.dumps(dictionary)
            file.write(line+'\n')

    # convert to parquet
    table = pj.read_json('/tmp/output_currency_dict.json')
    pq.write_table(table, '/tmp/formatted_dim_currency.parquet')

    return response
    