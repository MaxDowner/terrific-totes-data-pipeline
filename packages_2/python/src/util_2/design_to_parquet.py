from pyarrow import json as pj
import json
import pyarrow.parquet as pq

"""takes a list of updated data for design
    converts the data to parquet

    Args:
        updated_rows (list): list of updated design data
"""


def design_to_parquet(updated_rows: list):

    with open("/tmp/output_design_dict.json", 'w') as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + '\n')
    table = pj.read_json("/tmp/output_design_dict.json")
    pq.write_table(table, '/tmp/formatted_dim_design.parquet')
