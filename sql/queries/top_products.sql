-- Top 10 Performing Product Categories by Net Revenue & Units Sold
SELECT 
    p.category,
    p.subcategory,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.net_amount) AS total_net_revenue,
    ROUND(AVG(f.net_amount), 2) AS avg_order_value
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2026
GROUP BY p.category, p.subcategory
ORDER BY total_net_revenue DESC
LIMIT 10;
