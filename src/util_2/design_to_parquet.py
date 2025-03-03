from pyarrow import json as pj
import json
import pyarrow.parquet as pq
# {"design": [row_1, row_2, row_3]}

# row_1 = {"design_id": data_1, "design_name": data_2, "file_location": data_3, "file_name" : data_4}



def design_to_parquet(updated_rows: list):
    # each element in updated_rows is an updated row: dict
    output_dict = {"dim_design": updated_rows}

    with open("tmp/output_dict.json", 'w') as f:
        json.dump(output_dict, f)

    table = pj.read_json("tmp/output_dict.json") 
    pq.write_table(table, 'tmp/formatted_dim_designs.parquet')

# output -> "dim_design": [
    # {"design_id": data_1, "design_name": data_2, "file_location": data_3, "file_name" : data_4}
    # {"design_id": data_5, "design_name": data_6, "file_location": data_7, "file_name" : data_8}
    # {"design_id": data_9, "design_name": data_10, "file_location": data_11, "file_name" : data_12}
    # ]