from pyarrow import json as pj
import json
import pyarrow.parquet as pq

def process_staff(updated_rows: list):
    """takes a list of updated data for staff
    converts the data to parquet

    Args:
        updated_rows (list): list of updated staff data
    """
    # each element in updated_rows is an updated row: dict
    # output_dict = {"staff": updated_rows}
    with open("/tmp/output_staff_dict.json", 'w') as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + '\n')
    table = pj.read_json("/tmp/output_staff_dict.json") 
    pq.write_table(table, '/tmp/formatted_dim_staff.parquet')
