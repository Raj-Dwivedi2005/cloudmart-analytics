-- Customer Cohort Analysis: Retention & Lifetime Revenue by First Purchase Month
WITH customer_first_purchase AS (
    SELECT 
        c.customer_id,
        MIN(d.full_date) AS first_purchase_date,
        DATE_TRUNC('month', MIN(d.full_date)) AS cohort_month
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY c.customer_id
),
monthly_activity AS (
    SELECT 
        fp.cohort_month,
        DATE_TRUNC('month', d.full_date) AS activity_month,
        DATEDIFF('month', fp.cohort_month, DATE_TRUNC('month', d.full_date)) AS month_number,
        f.customer_key,
        f.net_amount
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN customer_first_purchase fp ON c.customer_id = fp.customer_id
)
SELECT 
    TO_CHAR(cohort_month, 'YYYY-MM') AS cohort,
    month_number,
    COUNT(DISTINCT customer_key) AS active_customers,
    ROUND(SUM(net_amount), 2) AS cohort_revenue
FROM monthly_activity
GROUP BY cohort_month, month_number
ORDER BY cohort_month ASC, month_number ASC;
