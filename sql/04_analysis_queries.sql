-- ============================================================
-- QuickBite Analytics – Script 04: Analysis Queries
-- Team: Data Knights | CODEGNAN DA-07
-- MySQL 8.0+ Compatible
-- ============================================================

USE quickbite_analytics;

-- ═══════════════════════════════════════════════════════════════
-- QUERY 01: Total Orders by City
-- Business Question: Which cities drive the most order volume?
-- ═══════════════════════════════════════════════════════════════
SELECT
    r.city,
    COUNT(o.order_id)                                   AS total_orders,
    SUM(CASE WHEN o.order_status = 'Completed'         THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN o.order_status = 'Cancelled'         THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)
        / COUNT(o.order_id) * 100, 2
    )                                                   AS cancellation_rate_pct,
    ROUND(COUNT(o.order_id) / SUM(COUNT(o.order_id)) OVER () * 100, 2)
                                                        AS pct_of_total
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.city
ORDER BY total_orders DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 02: Gross Order Value and Net Sales by City
-- Business Question: Where is QuickBite generating the most revenue?
-- ═══════════════════════════════════════════════════════════════
SELECT
    r.city,
    COUNT(o.order_id)                           AS total_orders,
    ROUND(SUM(o.order_value), 2)                AS gross_order_value_inr,
    ROUND(SUM(o.discount), 2)                   AS total_discounts_inr,
    ROUND(SUM(o.final_amount), 2)               AS net_sales_inr,
    ROUND(AVG(o.order_value), 2)                AS avg_order_value_inr,
    ROUND(SUM(o.discount) / SUM(o.order_value) * 100, 2)
                                                AS discount_rate_pct
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status IN ('Completed', 'Partially Delivered')
GROUP BY r.city
ORDER BY net_sales_inr DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 03: Restaurant Ranking by Total Completed Orders
-- Business Question: Which restaurants handle the highest volumes?
-- ═══════════════════════════════════════════════════════════════
WITH RestOrderCounts AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.cuisine,
        r.city,
        r.area,
        COUNT(o.order_id) AS completed_orders
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE o.order_status IN ('Completed', 'Partially Delivered')
    GROUP BY o.restaurant_id, r.restaurant_name, r.cuisine, r.city, r.area
)
SELECT
    RANK() OVER (ORDER BY completed_orders DESC) AS `rank`,
    restaurant_id,
    restaurant_name,
    cuisine,
    city,
    area,
    completed_orders
FROM RestOrderCounts
ORDER BY `rank`
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 04: Restaurant Ranking by Revenue
-- Business Question: Which restaurants generate the most revenue?
-- ═══════════════════════════════════════════════════════════════
WITH RestRevenue AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.cuisine,
        r.city,
        COUNT(o.order_id)          AS total_orders,
        ROUND(SUM(o.final_amount), 2) AS total_revenue_inr,
        ROUND(AVG(o.final_amount), 2) AS avg_order_value_inr
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE o.order_status IN ('Completed', 'Partially Delivered')
    GROUP BY o.restaurant_id, r.restaurant_name, r.cuisine, r.city
)
SELECT
    RANK() OVER (ORDER BY total_revenue_inr DESC) AS revenue_rank,
    restaurant_id,
    restaurant_name,
    cuisine,
    city,
    total_orders,
    total_revenue_inr,
    avg_order_value_inr
FROM RestRevenue
ORDER BY revenue_rank
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 05: Restaurant Ranking by Average Customer Rating
-- Business Question: Which restaurants have the best customer satisfaction?
-- ═══════════════════════════════════════════════════════════════
WITH RestRatings AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.cuisine,
        r.city,
        r.restaurant_rating                    AS platform_rating,
        COUNT(f.feedback_id)                   AS total_reviews,
        ROUND(AVG(f.rating), 2)                AS avg_customer_rating,
        SUM(CASE WHEN f.rating = 5 THEN 1 ELSE 0 END) AS five_star_count,
        SUM(CASE WHEN f.rating <= 2 THEN 1 ELSE 0 END) AS low_rating_count
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    LEFT JOIN feedback f ON o.order_id = f.order_id
    WHERE o.order_status IN ('Completed', 'Partially Delivered')
    GROUP BY o.restaurant_id, r.restaurant_name, r.cuisine, r.city, r.restaurant_rating
    HAVING total_reviews >= 10   -- minimum reviews for statistical reliability
)
SELECT
    RANK() OVER (ORDER BY avg_customer_rating DESC) AS rating_rank,
    restaurant_id,
    restaurant_name,
    cuisine,
    city,
    platform_rating,
    total_reviews,
    avg_customer_rating,
    ROUND(five_star_count / total_reviews * 100, 1)  AS pct_5_star,
    ROUND(low_rating_count / total_reviews * 100, 1) AS pct_low_rating
FROM RestRatings
ORDER BY rating_rank
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 06: Complaint Rate by Restaurant
-- Business Question: Which restaurants receive the most complaints?
-- ═══════════════════════════════════════════════════════════════
WITH RestComplaints AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.city,
        r.cuisine,
        COUNT(f.feedback_id)                                        AS total_feedback,
        SUM(CASE WHEN f.complaint_type IS NOT NULL
                  AND f.complaint_type != '' THEN 1 ELSE 0 END)    AS complaint_count,
        f.complaint_type,
        COUNT(f.complaint_type)                                     AS complaint_freq
    FROM orders o
    JOIN restaurants r   ON o.restaurant_id = r.restaurant_id
    LEFT JOIN feedback f ON o.order_id = f.order_id
    WHERE o.order_status IN ('Completed', 'Partially Delivered')
    GROUP BY o.restaurant_id, r.restaurant_name, r.city, r.cuisine, f.complaint_type
)
SELECT
    restaurant_id,
    restaurant_name,
    city,
    cuisine,
    SUM(total_feedback)                                            AS total_feedback,
    SUM(complaint_count)                                           AS total_complaints,
    ROUND(
        SUM(CASE WHEN complaint_type IS NOT NULL AND complaint_type != ''
            THEN complaint_freq ELSE 0 END)
        / NULLIF(SUM(total_feedback), 0) * 100, 2
    )                                                              AS complaint_rate_pct,
    GROUP_CONCAT(
        DISTINCT CASE WHEN complaint_type IS NOT NULL AND complaint_type != ''
        THEN complaint_type END
        ORDER BY complaint_freq DESC SEPARATOR ', '
    )                                                              AS top_complaints
FROM RestComplaints
GROUP BY restaurant_id, restaurant_name, city, cuisine
HAVING total_complaints > 0
ORDER BY complaint_rate_pct DESC
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 07: Average Delivery Time by City
-- Business Question: How fast are deliveries in each city?
-- ═══════════════════════════════════════════════════════════════
SELECT
    r.city,
    COUNT(d.delivery_id)                            AS total_deliveries,
    ROUND(AVG(d.actual_delivery_minutes), 1)        AS avg_delivery_time_min,
    ROUND(MIN(d.actual_delivery_minutes), 1)        AS min_delivery_time_min,
    ROUND(MAX(d.actual_delivery_minutes), 1)        AS max_delivery_time_min,
    ROUND(AVG(d.delay_minutes), 1)                  AS avg_delay_min,
    ROUND(AVG(d.distance_km), 2)                    AS avg_distance_km,
    SUM(CASE WHEN d.on_time_status = 'On Time' THEN 1 ELSE 0 END)
                                                    AS on_time_deliveries,
    ROUND(
        SUM(CASE WHEN d.on_time_status = 'On Time' THEN 1 ELSE 0 END)
        / COUNT(d.delivery_id) * 100, 2
    )                                               AS on_time_pct
FROM deliveries d
JOIN orders o      ON d.order_id      = o.order_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.city
ORDER BY avg_delivery_time_min;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 08: Average Delivery Time by Area and Hour
-- Business Question: When and where are deliveries slowest?
-- ═══════════════════════════════════════════════════════════════
SELECT
    r.city,
    r.area,
    HOUR(o.order_time)                          AS order_hour,
    COUNT(d.delivery_id)                        AS total_deliveries,
    ROUND(AVG(d.actual_delivery_minutes), 1)    AS avg_delivery_time_min,
    ROUND(AVG(d.delay_minutes), 1)              AS avg_delay_min,
    ROUND(
        SUM(CASE WHEN d.on_time_status = 'Delayed' THEN 1 ELSE 0 END)
        / COUNT(d.delivery_id) * 100, 1
    )                                           AS delay_rate_pct
FROM deliveries d
JOIN orders o      ON d.order_id      = o.order_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.city, r.area, HOUR(o.order_time)
HAVING total_deliveries >= 5
ORDER BY avg_delay_min DESC
LIMIT 50;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 09: Identify Slow-Performing Delivery Areas
-- Business Question: Which areas consistently have the worst delivery performance?
-- ═══════════════════════════════════════════════════════════════
WITH AreaPerf AS (
    SELECT
        r.city,
        r.area,
        COUNT(d.delivery_id)                        AS total_deliveries,
        ROUND(AVG(d.actual_delivery_minutes), 1)    AS avg_delivery_time,
        ROUND(AVG(d.delay_minutes), 1)              AS avg_delay,
        ROUND(
            SUM(CASE WHEN d.on_time_status = 'Delayed' THEN 1 ELSE 0 END)
            / COUNT(d.delivery_id) * 100, 2
        )                                           AS delay_rate_pct,
        AVG(AVG(d.actual_delivery_minutes)) OVER (PARTITION BY r.city)
                                                    AS city_avg_delivery
    FROM deliveries d
    JOIN orders o      ON d.order_id      = o.order_id
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    GROUP BY r.city, r.area
    HAVING total_deliveries >= 50
)
SELECT
    city,
    area,
    total_deliveries,
    avg_delivery_time,
    avg_delay,
    delay_rate_pct,
    ROUND(avg_delivery_time - city_avg_delivery, 1) AS time_above_city_avg,
    RANK() OVER (PARTITION BY city ORDER BY delay_rate_pct DESC) AS area_delay_rank
FROM AreaPerf
ORDER BY city, area_delay_rank;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 10: Cancellation Rate by Restaurant
-- Business Question: Which restaurants have the highest cancellation rates?
-- ═══════════════════════════════════════════════════════════════
WITH RestCancel AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.city,
        r.cuisine,
        COUNT(o.order_id)                                           AS total_orders,
        SUM(CASE WHEN o.order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
                                                                    AS cancelled_orders,
        ROUND(
            SUM(CASE WHEN o.order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
            / COUNT(o.order_id) * 100, 2
        )                                                           AS cancellation_rate_pct
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    GROUP BY o.restaurant_id, r.restaurant_name, r.city, r.cuisine
    HAVING total_orders >= 20   -- minimum sample size
)
SELECT
    RANK() OVER (ORDER BY cancellation_rate_pct DESC) AS `rank`,
    restaurant_id,
    restaurant_name,
    city,
    cuisine,
    total_orders,
    cancelled_orders,
    cancellation_rate_pct
FROM RestCancel
ORDER BY cancellation_rate_pct DESC
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 11: Most Common Cancellation Reasons
-- Business Question: Why are customers cancelling orders?
-- ═══════════════════════════════════════════════════════════════
SELECT
    cancellation_reason,
    COUNT(*)                                            AS total_cancellations,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 2)  AS pct_of_total,
    ROUND(AVG(order_value), 2)                         AS avg_order_value_inr
FROM orders
WHERE order_status IN ('Cancelled', 'Refunded')
  AND cancellation_reason IS NOT NULL
  AND cancellation_reason != ''
GROUP BY cancellation_reason
ORDER BY total_cancellations DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 12: Repeat Customer Rate by City
-- Business Question: How many customers are retained vs one-time users?
-- ═══════════════════════════════════════════════════════════════
WITH CustomerOrderCounts AS (
    SELECT
        o.customer_id,
        c.city,
        COUNT(o.order_id) AS order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.city
)
SELECT
    city,
    COUNT(customer_id)                                                   AS total_customers,
    SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END)                   AS one_time_customers,
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END)                  AS repeat_customers,
    SUM(CASE WHEN order_count >= 5 THEN 1 ELSE 0 END)                  AS loyal_customers_5plus,
    SUM(CASE WHEN order_count >= 10 THEN 1 ELSE 0 END)                 AS vip_customers_10plus,
    ROUND(
        SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END)
        / COUNT(customer_id) * 100, 2
    )                                                                    AS repeat_rate_pct,
    ROUND(AVG(order_count), 2)                                          AS avg_orders_per_customer
FROM CustomerOrderCounts
GROUP BY city
ORDER BY repeat_rate_pct DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 13: Repeat vs One-Time Customer Revenue Comparison
-- Business Question: How much more valuable are repeat customers?
-- ═══════════════════════════════════════════════════════════════
WITH CustomerSegments AS (
    SELECT
        o.customer_id,
        COUNT(o.order_id)          AS order_count,
        SUM(o.final_amount)        AS total_spend,
        AVG(o.final_amount)        AS avg_order_value
    FROM orders o
    WHERE o.order_status IN ('Completed', 'Partially Delivered')
    GROUP BY o.customer_id
)
SELECT
    CASE
        WHEN order_count = 1  THEN '1 - One-time Customer'
        WHEN order_count <= 3 THEN '2-3 Orders'
        WHEN order_count <= 9 THEN '4-9 Orders (Regular)'
        ELSE '10+ Orders (Loyal/VIP)'
    END                                              AS customer_segment,
    COUNT(customer_id)                               AS customer_count,
    ROUND(SUM(total_spend), 2)                       AS segment_revenue_inr,
    ROUND(AVG(total_spend), 2)                       AS avg_lifetime_value_inr,
    ROUND(AVG(avg_order_value), 2)                   AS avg_order_value_inr,
    ROUND(
        SUM(total_spend) / SUM(SUM(total_spend)) OVER () * 100, 2
    )                                                AS pct_of_total_revenue
FROM CustomerSegments
GROUP BY customer_segment
ORDER BY customer_segment;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 14: Delivery Time vs Customer Ratings
-- Business Question: Does delivery delay negatively impact ratings?
-- ═══════════════════════════════════════════════════════════════
SELECT
    CASE
        WHEN d.delay_minutes <= 0      THEN 'Early (<=0 min)'
        WHEN d.delay_minutes <= 5      THEN 'On Time (1-5 min)'
        WHEN d.delay_minutes <= 15     THEN 'Slight Delay (6-15 min)'
        WHEN d.delay_minutes <= 30     THEN 'Moderate Delay (16-30 min)'
        WHEN d.delay_minutes <= 60     THEN 'Significant Delay (31-60 min)'
        ELSE 'Severe Delay (>60 min)'
    END                                              AS delay_bucket,
    COUNT(f.feedback_id)                             AS feedback_count,
    ROUND(AVG(f.rating), 2)                         AS avg_rating,
    ROUND(AVG(d.delay_minutes), 1)                  AS avg_delay_min,
    SUM(CASE WHEN f.rating >= 4 THEN 1 ELSE 0 END)  AS high_ratings,
    SUM(CASE WHEN f.rating <= 2 THEN 1 ELSE 0 END)  AS low_ratings,
    ROUND(
        SUM(CASE WHEN f.rating >= 4 THEN 1 ELSE 0 END)
        / COUNT(f.feedback_id) * 100, 1
    )                                                AS pct_high_rating,
    ROUND(
        SUM(CASE WHEN f.rating <= 2 THEN 1 ELSE 0 END)
        / COUNT(f.feedback_id) * 100, 1
    )                                                AS pct_low_rating
FROM deliveries d
JOIN orders  o ON d.order_id = o.order_id
JOIN feedback f ON o.order_id = f.order_id
GROUP BY delay_bucket
ORDER BY avg_delay_min;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 15: Distance vs Delivery Delays
-- Business Question: Do longer distances cause more delays?
-- ═══════════════════════════════════════════════════════════════
SELECT
    CASE
        WHEN d.distance_km <= 2    THEN '0-2 km (Very Close)'
        WHEN d.distance_km <= 5    THEN '2-5 km (Close)'
        WHEN d.distance_km <= 8    THEN '5-8 km (Medium)'
        WHEN d.distance_km <= 12   THEN '8-12 km (Far)'
        ELSE '12+ km (Very Far)'
    END                                              AS distance_bucket,
    COUNT(d.delivery_id)                             AS total_deliveries,
    ROUND(AVG(d.actual_delivery_minutes), 1)         AS avg_delivery_time_min,
    ROUND(AVG(d.delay_minutes), 1)                   AS avg_delay_min,
    ROUND(
        SUM(CASE WHEN d.on_time_status = 'Delayed' THEN 1 ELSE 0 END)
        / COUNT(d.delivery_id) * 100, 2
    )                                                AS delay_rate_pct,
    ROUND(AVG(d.distance_km), 2)                     AS avg_distance_km
FROM deliveries d
GROUP BY distance_bucket
ORDER BY avg_distance_km;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 16: Peak Ordering Hours Analysis
-- Business Question: When do customers order the most?
-- ═══════════════════════════════════════════════════════════════
SELECT
    HOUR(order_time)                                 AS hour_of_day,
    CASE
        WHEN HOUR(order_time) BETWEEN 6  AND 11 THEN 'Morning (6-11)'
        WHEN HOUR(order_time) BETWEEN 12 AND 14 THEN 'Lunch Peak (12-14)'
        WHEN HOUR(order_time) BETWEEN 15 AND 17 THEN 'Afternoon (15-17)'
        WHEN HOUR(order_time) BETWEEN 18 AND 22 THEN 'Dinner Peak (18-22)'
        ELSE 'Late Night / Early Morning'
    END                                              AS time_segment,
    COUNT(order_id)                                  AS total_orders,
    SUM(CASE WHEN order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
                                                     AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
        / COUNT(order_id) * 100, 2
    )                                                AS cancellation_rate_pct,
    ROUND(AVG(final_amount), 2)                      AS avg_order_value_inr,
    ROUND(COUNT(order_id) / SUM(COUNT(order_id)) OVER () * 100, 2)
                                                     AS pct_of_daily_orders
FROM orders
GROUP BY HOUR(order_time), time_segment
ORDER BY hour_of_day;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 17: Restaurants with Consistently Poor Performance
-- Business Question: Which restaurants need urgent intervention?
-- ═══════════════════════════════════════════════════════════════
WITH RestPerf AS (
    SELECT
        o.restaurant_id,
        r.restaurant_name,
        r.city,
        r.cuisine,
        r.avg_prep_time,
        COUNT(o.order_id)                                               AS total_orders,
        ROUND(AVG(f.rating), 2)                                         AS avg_rating,
        ROUND(
            SUM(CASE WHEN o.order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
            / COUNT(o.order_id) * 100, 2
        )                                                               AS cancel_rate_pct,
        ROUND(
            SUM(CASE WHEN f.complaint_type IS NOT NULL AND f.complaint_type != ''
                THEN 1 ELSE 0 END)
            / NULLIF(COUNT(f.feedback_id), 0) * 100, 2
        )                                                               AS complaint_rate_pct,
        ROUND(AVG(d.actual_delivery_minutes), 1)                        AS avg_delivery_min,
        ROUND(SUM(f.refund_amount), 2)                                  AS total_refunds_inr
    FROM orders o
    JOIN restaurants r  ON o.restaurant_id = r.restaurant_id
    LEFT JOIN feedback f ON o.order_id = f.order_id
    LEFT JOIN deliveries d ON o.order_id = d.order_id
    GROUP BY
        o.restaurant_id, r.restaurant_name, r.city, r.cuisine, r.avg_prep_time
    HAVING total_orders >= 20
),
PerfScored AS (
    SELECT *,
        -- Poor performance = low rating AND high cancellation AND high complaints
        (CASE WHEN avg_rating < 3.0      THEN 1 ELSE 0 END) +
        (CASE WHEN cancel_rate_pct > 15  THEN 1 ELSE 0 END) +
        (CASE WHEN complaint_rate_pct > 20 THEN 1 ELSE 0 END)  AS poor_perf_flags
    FROM RestPerf
)
SELECT
    restaurant_id,
    restaurant_name,
    city,
    cuisine,
    total_orders,
    avg_rating,
    cancel_rate_pct,
    complaint_rate_pct,
    avg_delivery_min,
    total_refunds_inr,
    poor_perf_flags,
    CASE poor_perf_flags
        WHEN 3 THEN 'CRITICAL - All 3 flags'
        WHEN 2 THEN 'HIGH - 2 flags'
        WHEN 1 THEN 'MODERATE - 1 flag'
        ELSE 'OK'
    END AS performance_status
FROM PerfScored
WHERE poor_perf_flags >= 1
ORDER BY poor_perf_flags DESC, avg_rating ASC
LIMIT 30;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 18: Highest-Performing Cuisines
-- Business Question: Which cuisines drive the most orders and revenue?
-- ═══════════════════════════════════════════════════════════════
SELECT
    r.cuisine,
    COUNT(DISTINCT r.restaurant_id)                  AS restaurant_count,
    COUNT(o.order_id)                                AS total_orders,
    SUM(CASE WHEN o.order_status IN ('Completed','Partially Delivered') THEN 1 ELSE 0 END)
                                                     AS completed_orders,
    ROUND(SUM(CASE WHEN o.order_status IN ('Completed','Partially Delivered')
        THEN o.final_amount ELSE 0 END), 2)          AS total_revenue_inr,
    ROUND(AVG(CASE WHEN o.order_status IN ('Completed','Partially Delivered')
        THEN o.final_amount END), 2)                 AS avg_order_value_inr,
    ROUND(AVG(f.rating), 2)                          AS avg_customer_rating,
    ROUND(AVG(r.avg_prep_time), 1)                   AS avg_prep_time_min,
    ROUND(
        SUM(CASE WHEN o.order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
        / COUNT(o.order_id) * 100, 2
    )                                                AS cancellation_rate_pct
FROM restaurants r
JOIN orders   o ON r.restaurant_id = o.restaurant_id
LEFT JOIN feedback f ON o.order_id = f.order_id
GROUP BY r.cuisine
ORDER BY total_revenue_inr DESC;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 19: Refund Analysis by City and Restaurant
-- Business Question: Where is QuickBite losing money to refunds?
-- ═══════════════════════════════════════════════════════════════
-- 19a. Refunds by City
SELECT
    r.city,
    COUNT(f.feedback_id)                        AS feedback_count,
    SUM(CASE WHEN f.refund_amount > 0 THEN 1 ELSE 0 END)
                                                AS refund_issued_count,
    ROUND(SUM(f.refund_amount), 2)              AS total_refund_inr,
    ROUND(AVG(CASE WHEN f.refund_amount > 0 THEN f.refund_amount END), 2)
                                                AS avg_refund_when_issued_inr,
    ROUND(
        SUM(CASE WHEN f.refund_amount > 0 THEN 1 ELSE 0 END)
        / COUNT(f.feedback_id) * 100, 2
    )                                           AS refund_rate_pct
FROM feedback f
JOIN orders      o ON f.order_id      = o.order_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.city
ORDER BY total_refund_inr DESC;

-- 19b. Top 20 Restaurants by Total Refunds
SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine,
    COUNT(f.feedback_id)                                    AS total_feedback,
    SUM(CASE WHEN f.refund_amount > 0 THEN 1 ELSE 0 END)   AS refund_count,
    ROUND(SUM(f.refund_amount), 2)                          AS total_refund_inr,
    ROUND(AVG(f.rating), 2)                                 AS avg_rating
FROM feedback f
JOIN orders      o ON f.order_id      = o.order_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name, r.city, r.cuisine
HAVING total_refund_inr > 0
ORDER BY total_refund_inr DESC
LIMIT 20;


-- ═══════════════════════════════════════════════════════════════
-- QUERY 20: Consolidated Restaurant Performance Report
-- Business Question: Full 360° view of each restaurant's health
-- ═══════════════════════════════════════════════════════════════
WITH RestFull AS (
    SELECT
        r.restaurant_id,
        r.restaurant_name,
        r.cuisine,
        r.city,
        r.area,
        r.avg_prep_time,
        r.restaurant_rating                                     AS platform_rating,

        -- Order metrics
        COUNT(DISTINCT o.order_id)                              AS total_orders,
        SUM(CASE WHEN o.order_status IN ('Completed','Partially Delivered') THEN 1 ELSE 0 END)
                                                                AS completed_orders,
        ROUND(
            SUM(CASE WHEN o.order_status IN ('Cancelled','Refunded') THEN 1 ELSE 0 END)
            / NULLIF(COUNT(o.order_id), 0) * 100, 2
        )                                                       AS cancel_rate_pct,

        -- Revenue metrics
        ROUND(SUM(CASE WHEN o.order_status IN ('Completed','Partially Delivered')
            THEN o.final_amount ELSE 0 END), 2)                AS total_revenue_inr,
        ROUND(AVG(CASE WHEN o.order_status IN ('Completed','Partially Delivered')
            THEN o.final_amount END), 2)                        AS avg_order_value_inr,

        -- Delivery metrics
        ROUND(AVG(d.actual_delivery_minutes), 1)                AS avg_delivery_min,
        ROUND(
            SUM(CASE WHEN d.on_time_status = 'On Time' THEN 1 ELSE 0 END)
            / NULLIF(COUNT(d.delivery_id), 0) * 100, 2
        )                                                       AS on_time_pct,

        -- Customer satisfaction metrics
        ROUND(AVG(f.rating), 2)                                 AS avg_customer_rating,
        COUNT(DISTINCT f.feedback_id)                           AS total_reviews,
        ROUND(
            SUM(CASE WHEN f.complaint_type IS NOT NULL AND f.complaint_type != ''
                THEN 1 ELSE 0 END)
            / NULLIF(COUNT(f.feedback_id), 0) * 100, 2
        )                                                       AS complaint_rate_pct,
        ROUND(SUM(f.refund_amount), 2)                          AS total_refund_inr

    FROM restaurants r
    LEFT JOIN orders     o  ON r.restaurant_id = o.restaurant_id
    LEFT JOIN deliveries d  ON o.order_id = d.order_id
    LEFT JOIN feedback   f  ON o.order_id = f.order_id
    GROUP BY
        r.restaurant_id, r.restaurant_name, r.cuisine, r.city,
        r.area, r.avg_prep_time, r.restaurant_rating
    HAVING total_orders >= 10
),
RankedPerf AS (
    SELECT *,
        DENSE_RANK() OVER (PARTITION BY city ORDER BY avg_customer_rating DESC)
            AS city_rating_rank,
        DENSE_RANK() OVER (PARTITION BY city ORDER BY total_revenue_inr DESC)
            AS city_revenue_rank,
        DENSE_RANK() OVER (PARTITION BY city ORDER BY cancel_rate_pct ASC)
            AS city_reliability_rank,
        CASE
            WHEN avg_customer_rating >= 4.0 AND cancel_rate_pct < 10 AND on_time_pct > 80
                THEN 'TOP PERFORMER'
            WHEN avg_customer_rating < 3.0 OR cancel_rate_pct > 20 OR complaint_rate_pct > 25
                THEN 'NEEDS ATTENTION'
            ELSE 'AVERAGE'
        END AS performance_tier
    FROM RestFull
)
SELECT
    restaurant_id, restaurant_name, cuisine, city, area,
    avg_prep_time, platform_rating,
    total_orders, completed_orders, cancel_rate_pct,
    total_revenue_inr, avg_order_value_inr,
    avg_delivery_min, on_time_pct,
    avg_customer_rating, total_reviews, complaint_rate_pct, total_refund_inr,
    city_rating_rank, city_revenue_rank, city_reliability_rank,
    performance_tier
FROM RankedPerf
ORDER BY performance_tier, avg_customer_rating DESC;
