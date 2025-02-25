from pprint import pprint
from datetime import datetime

from src.util.pg_connection import connect_to_db, close_connection

# query_dict = {
#     "1": "SELECT currency_id, currency_code FROM currency WHERE last_updated < :time;"
# }

def lambda_handler(event, context):
    db = None
    try:
        db = connect_to_db()
        time = str(datetime.now())
        query = """SELECT currency_id, currency_code FROM currency WHERE last_updated < :time;"""

        result = db.run(query, time=time)
        pprint(result)

    except:
        # log failure here
        pass

    finally:
        close_connection(db)


lambda_handler({}, {})
