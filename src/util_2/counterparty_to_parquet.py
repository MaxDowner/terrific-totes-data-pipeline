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
from copy import deepcopy


def counterparty_to_parquet(updated_rows: list):
    """
    takes a list of updated data for counterparty
    converts the data to parquet

    Args:
        updated_rows (list): list of updated counterparty data
    """
    safe_list = []
    for row in updated_rows:
        safe_row = deepcopy(row)
        for key in row:
            if not key.startswith("counterparty"):
                if key == "phone":
                    safe_row["counterparty_legal_phone_number"
                             ] = safe_row.pop("phone")
                else:
                    safe_row[f'counterparty_legal_{key}'] = safe_row.pop(key)
        safe_list.append(safe_row)

    with open("/tmp/output_counterparty_dict.json", "w") as f:
        for dict in safe_list:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_counterparty_dict.json")
    pq.write_table(table, "/tmp/formatted_dim_counterparty.parquet")
