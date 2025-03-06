# "address_id",
# "address_line_1",
# "address_line_2",
# "district",
# "city",
# "postal_code",
# "country",
# "phone",

from pyarrow import json as pj
import json
import pyarrow.parquet as pq


def address_to_parquet(updated_rows: list):
    """takes a list of updated data for addresses
    converts the data to parquet

    Args:
        updated_rows (list): list of updated address data
    """

    with open("/tmp/output_address_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_address_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_address.parquet")
