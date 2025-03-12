from pyarrow import json as pj
import json
import pyarrow.parquet as pq


def address_to_parquet(updated_rows: list):
    """Transform ingested address data into the required format
    and file type and save in tmp.
    Takes a list of updated data for addresses
    Replaces address_id with location iD
    converts the data to parquet
    Saves parquet data in the tmp folder

    Args:
        updated_rows (list): list of updated address data
    """

    for row in updated_rows:
        row["location_id"] = row.pop("address_id")

    with open("/tmp/output_address_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_address_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_location.parquet")
