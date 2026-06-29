SELECT
    region,
    category,
    date_trunc('month', order_date) AS month,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount,
    COUNT(order_id) AS order_count
FROM {{ ref('stg_orders') }}
GROUP BY region, category, month
ORDER BY month, region, category
