
  
    
    

    create  table
      "superstore"."analytics"."sales_summary__dbt_tmp"
  
    as (
      SELECT
    region,
    category,
    date_trunc('month', order_date) AS month,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount,
    COUNT(order_id) AS order_count
FROM "superstore"."analytics"."stg_orders"
GROUP BY region, category, month
ORDER BY month, region, category
    );
  
  