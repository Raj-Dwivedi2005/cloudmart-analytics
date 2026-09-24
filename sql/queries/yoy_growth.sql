-- Year-over-Year (YoY) Revenue Growth & Quarterly Performance Comparison
WITH quarterly_revenue AS (
    SELECT 
        d.year,
        d.quarter,
        SUM(f.net_amount) AS total_revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.quarter
)
SELECT 
    curr.year AS current_year,
    curr.quarter AS quarter,
    curr.total_revenue AS current_revenue,
    prev.total_revenue AS prior_year_revenue,
    ROUND(curr.total_revenue - prev.total_revenue, 2) AS absolute_growth,
    ROUND(
        ((curr.total_revenue - prev.total_revenue) / NULLIF(prev.total_revenue, 0)) * 100, 
        2
    ) AS yoy_growth_percentage
FROM quarterly_revenue curr
LEFT JOIN quarterly_revenue prev 
    ON curr.quarter = prev.quarter 
   AND curr.year = prev.year + 1
ORDER BY current_year DESC, quarter ASC;
