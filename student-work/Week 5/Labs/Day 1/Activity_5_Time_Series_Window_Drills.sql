-- Activity 5: Time Series Window Drills (SQL)

-- Setup
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE SCHEMA TECHCATALYST.STOCKS;

SELECT COUNT(*) FROM GOOGLE_STOCKS;    -- 624
SELECT COUNT(*) FROM CLOSING_PRICE;    -- 504
SELECT COUNT(*) FROM MILK_PRODUCTION;  -- 168

-- G1: Each day's close, the previous close, the daily change, and the percent change (round 2).
-- Window tool: LAG(close) OVER (ORDER BY date)
SELECT DATE, CLOSE, 
    LAG(CLOSE) OVER (ORDER BY DATE) as previous_close, 
    CLOSE - previous_close as daily_change, 
    ROUND((daily_change / previous_close * 100), 2) as percent_change
FROM GOOGLE_STOCKS
LIMIT 10;

-- G2: A 30-day moving average (round 2) and a running maximum of the close.
-- frame ROWS BETWEEN 29 PRECEDING AND CURRENT ROW; running max needs no frame
SELECT DATE, CLOSE, 
    ROUND(AVG(CLOSE) OVER (ORDER BY DATE ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 2) as moving_avg_30_days, 
    MAX(CLOSE) OVER (ORDER BY DATE) as running_maximum
FROM GOOGLE_STOCKS
LIMIT 10;

-- G3: The single best day: the row where the daily change is the largest. HINT: consider using CTE
-- QUALIFY daily_change = MAX(daily_change) OVER ()
-- April 26, 2024
WITH daily_changes AS (
SELECT DATE, CLOSE, 
    LAG(CLOSE) OVER (ORDER BY DATE) as previous_close, 
    CLOSE - previous_close as daily_change,
FROM GOOGLE_STOCKS
)
SELECT *
FROM daily_changes
WHERE daily_change IS NOT NULL
ORDER BY daily_change DESC
LIMIT 1;
