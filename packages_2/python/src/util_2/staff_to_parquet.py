from pyarrow import json as pj
import json
import pyarrow.parquet as pq
import pyarrow as pa


def process_staff(updated_rows: list):
    """takes a list of updated data for staff
    converts the data to parquet

    Args:
        updated_rows (list): list of updated staff data
    """
    # each element in updated_rows is an updated row: dict
    # output_dict = {"staff": updated_rows}
    # Schema and casting is to remove time from date
    raw_schema = pa.schema([
        pa.field('staff_id', pa.int64()),
        pa.field('first_name', pa.string()),
        pa.field('last_name', pa.string()),
        pa.field('department_name', pa.string()),
        pa.field('location', pa.string()),
        pa.field('email_address', pa.string())
    ])
    processed_schema = pa.schema([
        pa.field('staff_id', pa.int32()),
        pa.field('first_name', pa.string()),
        pa.field('last_name', pa.string()),
        pa.field('department_name', pa.string()),
        pa.field('location', pa.string()),
        pa.field('email_address', pa.string())
    ])

    with open("/tmp/output_staff_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    raw_table = pj.read_json(
        "/tmp/output_staff_dict.json",
        parse_options=pj.ParseOptions(explicit_schema=raw_schema)
        )
    table = raw_table.cast(processed_schema)
    pq.write_table(table, "/tmp/formatted_dim_staff.parquet")
