from pyarrow import json as pj
import json
import pyarrow.parquet as pq

def process_staff(updated_rows: list):
    # each element in updated_rows is an updated row: dict
    output_dict = {"staff": updated_rows}
    print(updated_rows)
    with open("/tmp/output_staff_dict.json", 'w') as f:
        # json.dump(output_dict, f)
        json_str = ""
        # f.writelines(updated_rows)
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + '\n')
            # json_str += str(dict) + '\n'
        print(json_str)
        # # json.dump(json_str, f)


    table = pj.read_json("/tmp/output_staff_dict.json") 
    pq.write_table(table, '/tmp/formatted_dim_staff.parquet')
