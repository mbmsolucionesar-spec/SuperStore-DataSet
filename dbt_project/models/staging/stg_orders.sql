{{ config(materialized='view') }}

SELECT
    "Row ID" AS row_id,
    "Order ID" AS order_id,
    STRPTIME("Order Date", '%m/%d/%Y') AS order_date,
    STRPTIME("Ship Date", '%m/%d/%Y') AS ship_date,
    "Ship Mode" AS ship_mode,
    "Customer ID" AS customer_id,
    "Customer Name" AS customer_name,
    "Segment" AS segment,
    "Country/Region" AS country_region,
    "City" AS city,
    "State/Province" AS state_province,
    "Postal Code" AS postal_code,
    "Region" AS region,
    "Product ID" AS product_id,
    "Category" AS category,
    "Sub-Category" AS sub_category,
    "Product Name" AS product_name,
    CAST("Sales" AS DOUBLE) AS sales,
    CAST("Quantity" AS INTEGER) AS quantity,
    CAST("Discount" AS DOUBLE) AS discount,
    CAST("Profit" AS DOUBLE) AS profit
FROM raw_superstore
