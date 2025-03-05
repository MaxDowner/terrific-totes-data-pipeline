from pyarrow import json as pj
import json
import pyarrow.parquet as pq


# {
#     "sales_order_id": 121,
#     "staff_id": 18,  # >>>> sales_staff_id links to dim_staff
#     "counterparty_id": 5,  # >>>> links to dim_counterpart
#     "units_sold": 90219,
#     "unit_price": "3.96",
#     "currency_id": 2,  # >>>> links to dim_currency
#     "design_id": 26,  # >>>> links to dim_design
#     "agreed_delivery_date": "2022-12-17",  # >>>> links to dim_date
#     "agreed_payment_date": "2022-12-22",  # >>>> links to dim_date
#     "agreed_delivery_location_id": 8,  # >>>> links to dim_location
# }


def sales_to_parquet(updated_rows: list):
    """
    takes a list of updated data for salesS
    converts the data to parquet

    Args:
        updated_rows (list): list of updated sales data
    """

    with open("/tmp/output_sales_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    table = pj.read_json("/tmp/output_sales_dict.json")
    pq.write_table(table, "/tmp/formatted_fact_sales.parquet")
