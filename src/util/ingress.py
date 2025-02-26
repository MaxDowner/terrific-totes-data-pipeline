from src.util.pg_connection import connect_to_db, close_connection
from src.util.get_time_window import get_time_window

query_list = [
    """SELECT currency_id, currency_code FROM currency 
    WHERE last_updated BETWEEN :time_last AND :time_now;"""
    ,
    """SELECT staff_id, 
    first_name, 
    last_name, 
    department_name, 
    location, 
    email_address 
    FROM staff 
    INNER JOIN department USING (department_id) 
    WHERE (staff.last_updated BETWEEN :time_last AND :time_now) 
    OR (department.last_updated BETWEEN :time_last AND :time_now);"""
    ,
    """SELECT design_id, 
    design_name, 
    file_location, 
    file_name
    FROM design 
    WHERE last_updated BETWEEN :time_last AND :time_now;"""
    ,
    """SELECT address_id, 
        address_line_1, 
        address_line_2,
        district,
        city,
        postal_code,
        country,
        phone  
        FROM address
        WHERE last_updated BETWEEN :time_last AND :time_now;"""
    ,
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
    OR (address.last_updated BETWEEN :time_last AND :time_now)"""
    ,
    """SELECT sales_order_id,
        staff_id, 
        counterparty_id, 
        units_sold, 
        unit_price, 
        currency_id,
        design_id,
        agreed_delivery_date,
        agreed_payment_date,
        agreed_delivery_location_id 
        FROM sales_order
        FULL OUTER JOIN
        staff USING (staff_id)
        FULL OUTER JOIN
        counterparty USING (counterparty_id)
        FULL OUTER JOIN
        design USING (design_id)
        FULL OUTER JOIN
        currency USING (currency_id) 
        WHERE sales_order.last_updated BETWEEN :time_last AND :time_now;
        """
    ]

def ingress_handler():
    db = None
    data_dump = []
    try:
        db = connect_to_db()
        time_last, time_now = get_time_window()
        # print(time_last, time_now)
        # time_last = "1970-01-01 00:00:00.000" # for testing to get all data, remove on prod
        for query in query_list:
            result = db.run(query, time_last=time_last, time_now=time_now)
            data_dump.append(result)
    except:
        # log failure here
        pass

    finally:
        if db:
            close_connection(db)

    return data_dump
