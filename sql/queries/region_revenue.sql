-- Region-Wise Net Revenue Contribution & Average Discount Breakdown
SELECT 
    r.region_name,
    r.country_code,
    COUNT(DISTINCT f.customer_key) AS unique_customers,
    SUM(f.gross_amount) AS total_gross_revenue,
    SUM(f.discount_amount) AS total_discounts,
    SUM(f.net_amount) AS total_net_revenue,
    ROUND((SUM(f.net_amount) / SUM(SUM(f.net_amount)) OVER()) * 100, 2) AS revenue_share_pct
FROM fact_sales f
JOIN dim_region r ON f.region_key = r.region_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2026
GROUP BY r.region_name, r.country_code
ORDER BY total_net_revenue DESC;
