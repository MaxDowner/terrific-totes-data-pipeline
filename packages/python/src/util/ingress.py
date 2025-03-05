from src.util.pg_connection_aws import connect_to_db, close_connection
from src.util.get_time_window_s3 import get_time_window

query_list = [
    """SELECT currency_id, currency_code FROM currency
     WHERE last_updated BETWEEN :time_last AND :time_now;""",
    """SELECT staff_id,
    first_name,
    last_name,
    department_name,
    location,
    email_address
     FROM staff
     INNER JOIN department USING (department_id)
     WHERE (staff.last_updated BETWEEN :time_last AND :time_now)
     OR (department.last_updated BETWEEN :time_last AND :time_now);""",
    """SELECT design_id,
    design_name,
    file_location,
    file_name
     FROM design
     WHERE last_updated BETWEEN :time_last AND :time_now;""",
    """SELECT address_id,
        address_line_1,
        address_line_2,
        district,
        city,
        postal_code,
        country,
        phone
         FROM address
         WHERE last_updated BETWEEN :time_last AND :time_now;""",
    """SELECT
         counterparty_id,
        counterparty_legal_name,
        address_line_1,
        address_line_2,
        district,
        city,
        postal_code,
        country,
        phone
         FROM counterparty
         INNER JOIN
         address ON counterparty.legal_address_id = address.address_id
        WHERE (counterparty.last_updated BETWEEN :time_last AND :time_now)
    OR (address.last_updated BETWEEN :time_last AND :time_now)""",
    """ SELECT sales_order_id,
        staff_id,
        counterparty_id,
        units_sold,
        unit_price,
        currency_id,
        design_id,
        agreed_delivery_date,
        agreed_payment_date,
        agreed_delivery_location_id,
        sales_order.created_at::date as created_date,
        sales_order.created_at::time as created_time,
        sales_order.last_updated::date as last_updated_date,
        sales_order.last_updated::time as last_updated_time
         FROM sales_order
         FULL OUTER JOIN
         staff USING (staff_id)
        FULL OUTER JOIN
        counterparty USING (counterparty_id)
        FULL OUTER JOIN
        design USING (design_id)
        FULL OUTER JOIN
        currency USING (currency_id)
         WHERE sales_order.last_updated BETWEEN :time_last AND :time_now;""",
]
table_list = ["currency",
              "staff",
              "design",
              "address",
              "counterparty",
              "sales_order"]
column_list = [
    ["currency_id", "currency_code"],
    [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ],
    ["design_id", "design_name", "file_location", "file_name"],
    [
        "address_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ],
    [
        "counterparty_id",
        "counterparty_legal_name",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ],
    [
        "sales_order_id",
        "staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_delivery_date",
        "agreed_payment_date",
        "agreed_delivery_location_id",
    ],
]


def ingress_handler(db_details, s3_client, bucket_name: str, log_key: str):
    """util func that connects to the db
    logs time in csv log
    checks for updated data
    adds headers as keys to dictionary
    returns list of dictionaries of updated data

    Returns:
        list: list of dictionaries to be processed
    """
    db = None
    data_dump = []
    try:
        db = connect_to_db(db_details)
        time_last, time_now = get_time_window(s3_client, bucket_name, log_key)
        # print(time_last, time_now)
        # for testing to get all data, remove on prod
        # time_last = "1970-01-01 00:00:00.000"
        for i in range(len(query_list)):
            updated_data = db.run(
                query_list[i], time_last=time_last, time_now=time_now
                )
            if i == 5:
                for row in updated_data:
                    row[4] = str(row[4])
            table_updates = [dict(zip(column_list[i], row))
                             for row in updated_data]
            data_dump.append({table_list[i]: table_updates})
        data_dump.append({"time_of_update": time_now})

    except Exception:
        # log failure here
        pass

    finally:
        if db:
            close_connection(db)

    return data_dump
