from pyarrow import json as pj
import json
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa


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
# {
#     "created_at": "", # >>>> from totesys
#     "last_updated": "" # >>>> from totesys
# }


def sales_to_parquet(updated_rows: list):
    """
    takes a list of updated data for salesS
    converts the data to parquet

    Args:
        updated_rows (list): list of updated sales data
    """
    # Schema and casting is to remove time from date
    raw_schema = pa.schema(
        [
            pa.field("sales_order_id", pa.int64()),
            pa.field("created_date", pa.string()),
            pa.field("created_time", pa.string()),
            pa.field("last_updated_date", pa.string()),
            pa.field("last_updated_time", pa.string()),
            pa.field("sales_staff_id", pa.int64()),
            pa.field("counterparty_id", pa.int64()),
            pa.field("units_sold", pa.int64()),
            pa.field("unit_price", pa.string()),
            pa.field("currency_id", pa.int64()),
            pa.field("design_id", pa.int64()),
            pa.field("agreed_payment_date", pa.string()),
            pa.field("agreed_delivery_date", pa.string()),
            pa.field("agreed_delivery_location_id", pa.int64()),
        ]
    )
    processed_schema = pa.schema(
        [
            pa.field("sales_order_id", pa.int64()),
            pa.field("created_date", pa.date32()),
            pa.field("created_time", pa.string()),
            pa.field("last_updated_date", pa.date32()),
            pa.field("last_updated_time", pa.string()),
            pa.field("sales_staff_id", pa.int64()),
            pa.field("counterparty_id", pa.int64()),
            pa.field("units_sold", pa.int64()),
            pa.field("unit_price", pa.float64()),
            pa.field("currency_id", pa.int64()),
            pa.field("design_id", pa.int64()),
            pa.field("agreed_payment_date", pa.date32()),
            pa.field("agreed_delivery_date", pa.date32()),
            pa.field("agreed_delivery_location_id", pa.int64()),
        ]
    )
    with open("/tmp/output_sales_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    raw_table = pj.read_json(
        "/tmp/output_sales_dict.json",
        parse_options=pj.ParseOptions(explicit_schema=raw_schema),
    )
    table = raw_table.cast(processed_schema)
    print(table)
    table.set_column(
        table.schema.get_field_index("created_time"),
        "created_time",
        pc.strptime(table["created_time"], format="%H-%M-%S", unit="s").cast(
            pa.time32("s")
        ),
    )

    print(table)

    pq.write_table(table, "/tmp/formatted_fact_sales.parquet")


if __name__ == "__main__":
    updated_rows = [
        {
            "sales_order_id": 12296,
            "created_date": "2025-01-23",
            "created_time": "12:51:10",
            "last_updated_date": "2025-01-23",
            "last_updated_time": "12:51:10",
            "sales_staff_id": 5,
            "counterparty_id": 13,
            "units_sold": 91436,
            "unit_price": "3.51",
            "currency_id": 3,
            "design_id": 280,
            "agreed_delivery_date": "2025-01-29",
            "agreed_payment_date": "2025-01-24",
            "agreed_delivery_location_id": 26,
        }
    ]
    sales_to_parquet(updated_rows)
