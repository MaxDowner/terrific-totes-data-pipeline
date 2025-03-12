from pyarrow import json as pj
import json
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa


def sales_to_parquet(updated_rows: list):
    """Transform ingested sales data into the required format
    and file type and save in `/tmp/`.
    takes a list of updated data for salesS
    replace the staff_id header with sales_staff_id
    converts the data to parquet
    saves to `/tmp/` folder

    Args:
        updated_rows (list): list of updated sales data
    """

    for row in updated_rows:
        row["sales_staff_id"] = row.pop("staff_id")

    for item in updated_rows:
        item['created_time'] = item['created_time'][:7]
        item['last_updated_time'] = item['last_updated_time'][:7]

    # Schema and casting is to remove time from date
    raw_schema = pa.schema([
        pa.field('sales_order_id', pa.int64()),
        pa.field('created_date', pa.string()),
        pa.field('created_time', pa.string()),
        pa.field('last_updated_date', pa.string()),
        pa.field('last_updated_time', pa.string()),
        pa.field('sales_staff_id', pa.int64()),
        pa.field('counterparty_id', pa.int64()),
        pa.field('units_sold', pa.int64()),
        pa.field('unit_price', pa.string()),
        pa.field('currency_id', pa.int64()),
        pa.field('design_id', pa.int64()),
        pa.field('agreed_payment_date', pa.string()),
        pa.field('agreed_delivery_date', pa.string()),
        pa.field('agreed_delivery_location_id', pa.int64())
    ])
    processed_schema = pa.schema([
        pa.field('sales_order_id', pa.int64()),
        pa.field('created_date', pa.date32()),
        pa.field('created_time', pa.string()),
        pa.field('last_updated_date', pa.date32()),
        pa.field('last_updated_time', pa.string()),
        pa.field('sales_staff_id', pa.int64()),
        pa.field('counterparty_id', pa.int64()),
        pa.field('units_sold', pa.int64()),
        pa.field('unit_price', pa.decimal128(10, 2)),
        pa.field('currency_id', pa.int64()),
        pa.field('design_id', pa.int64()),
        pa.field('agreed_payment_date', pa.date32()),
        pa.field('agreed_delivery_date', pa.date32()),
        pa.field('agreed_delivery_location_id', pa.int64())
    ])
    with open("/tmp/output_sales_dict.json", "w") as f:
        for dict in updated_rows:
            line = json.dumps(dict)
            f.write(line + "\n")
    raw_table = pj.read_json(
        "/tmp/output_sales_dict.json",
        parse_options=pj.ParseOptions(explicit_schema=raw_schema)
        )
    table = raw_table.cast(processed_schema)

# Convert Created_time
    col_idx = table.schema.get_field_index("created_time")

    converted_time_column = pc.strptime(
        table["created_time"], format="%H:%M:%S", unit="s"
    ).cast(pa.time64("us"))

    # Replace the column in the table
    table = table.set_column(col_idx, "created_time", converted_time_column)

# Convert last_updated_time
    col_idx = table.schema.get_field_index("last_updated_time")

    converted_time_column = pc.strptime(
        table["last_updated_time"], format="%H:%M:%S", unit="s"
    ).cast(pa.time64("us"))

    # Replace the column in the table
    table = table.set_column(col_idx, "last_updated_time",
                             converted_time_column)

    print(table.schema)
    print(table)

    pq.write_table(table, "/tmp/formatted_fact_sales_order.parquet")
