from pyarrow import json
import pyarrow.parquet as pq

"""
NEED to make this run per table in json, not the entire json all at once
"""

table = json.read_json('/home/coachlamb92/northcoders/project/terrific-totes-data-pipeline/src/util_2/test.json') 

pq.write_table(table, 'test_results.parquet', )
