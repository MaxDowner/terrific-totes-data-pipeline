from pyarrow import json as pj
import json
import pyarrow.parquet as pq


def staff_to_parquet(updated_rows: list):
    """Transform ingested staff data into the required format
    and file type and save in `/tmp/`.
    takes a list of updated data for staff
    converts the data to parquet
    saves to `/tmp/` folder

    Args:
        updated_rows (list): list of updated staff data
    """
    with open("/tmp/output_staff_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_staff_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_staff.parquet")
