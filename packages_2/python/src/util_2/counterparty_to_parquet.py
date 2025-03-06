# counterparty_id,
# counterparty_legal_name,
# address_line_1,
# address_line_2,
# district,
# city,
# postal_code,
# country,
# phone

from pyarrow import json as pj
import json
import pyarrow.parquet as pq


def counterparty_to_parquet(updated_rows: list):
    """
    takes a list of updated data for counterparty
    converts the data to parquet

    Args:
        updated_rows (list): list of updated counterparty data
    """

    with open("/tmp/output_counterparty_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_counterparty_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_counterparty.parquet")
