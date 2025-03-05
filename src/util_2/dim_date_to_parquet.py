from src.util.pg_connection_aws import connect_to_db, close_connection
import pg8000
import boto3
from src.util.get_secret import get_secret
import pandas as pd
import json
from pyarrow import json as pj
import pyarrow.parquet as pq


query = """
        SELECT 
        day AS date_id,
        EXTRACT(YEAR FROM day)::INTEGER  AS year,
        EXTRACT(MONTH FROM day)::INTEGER  AS month,
        EXTRACT(DAY FROM day)::INTEGER  as day,
        EXTRACT(ISODOW FROM day)::INTEGER AS day_of_week,
        TO_CHAR(day, 'Day') AS day_name,
        TO_CHAR(day, 'Month') as month_name,
        EXTRACT(QUARTER FROM day)::INTEGER  AS quarter
        FROM generate_series('2022-01-01'::date, '2030-12-31'::date, '1 day') AS day;
        """

def dim_date_creation(): 
    # db_details, s3_client, bucket_name
    """ util function that connects to database
    """
    db = None

    try:
        # get db details
        secret_name = "Tote-DB"
        region_name = "eu-west-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name=region_name
        )
        db_details = get_secret(client, secret_name)   

        # connect to db with secret
        conn = connect_to_db(db_details)

        # run the query
        dim_date = conn.run(query)

        # Manually assign columns
        column_names = [
                'date_id', 'year','month','day','day_of_week','day_name','month_name', 'quarter']
        
        data_list = [dict(zip(column_names, row)) for row in dim_date]

        conn.close()

        # create parquet file 

        with open("/tmp/output_dim_date.json", "w") as f:
            for dict in data_list:
                line = json.dumps(dict)
                f.write(line + "\n")
        table = pj.read_json("/tmp/output_dim_date.json")
        pq.write_table(table, "/tmp/formatted_dim_date.parquet")
    
    except Exception:
        # log failure here
        pass

    finally:
        if db:
            close_connection(db)
    

print(dim_date_creation())