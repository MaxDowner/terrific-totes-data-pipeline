import requests
import json
from pyarrow import json as pj
import pyarrow.parquet as pq


def currency_to_parquet(updated_rows: list):
    """
    takes a list of updated currencies
    calls a currency API
    adds a currency name to each dictionary
    converts the data to parquet

    Args:
        updated_rows (list): list of updated currencies
    """
    # make api call and save to response
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0"\
        "/currency-api@latest/v1/currencies.json"
    response = requests.get(url)

    object_response = response.json()
    # add currency name to dict for all currencies
    for dict in updated_rows:
        currency_code = dict["currency_code"].lower()
        currency_name = object_response[currency_code]
        dict["currency_name"] = currency_name

    # convert to json lines
    with open("/tmp/output_currency_dict.json", "w") as file:
        for dictionary in updated_rows:
            line = json.dumps(dictionary)
            file.write(line + "\n")

    # convert to parquet
    table = pj.read_json("/tmp/output_currency_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_currency.parquet")

    # return response
