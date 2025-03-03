import pandas as pd


df = pd.read_parquet('test_results.parquet')
df.to_json('check_json_2.json', orient='records')