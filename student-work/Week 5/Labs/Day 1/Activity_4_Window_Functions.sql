-- Activity 4: Window Functions
-- Week 5, Day 1
-- Schema: TECHCATALYST.ORLANDO

-- Context block (run first)
USE ROLE DE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TECHCATALYST;
USE SCHEMA TECHCATALYST.ORLANDO;

-- SETUP: Create the stock table
-- Trading days: 10

CREATE OR REPLACE TRANSIENT TABLE W5D1_STOCK (
  trade_date DATE,
  close_price NUMBER(10, 2)
);

INSERT INTO W5D1_STOCK (trade_date, close_price) VALUES
  ('2024-07-01', 100),
  ('2024-07-02', 102),
  ('2024-07-03', 101),
  ('2024-07-04', 105),
  ('2024-07-05', 103),
  ('2024-07-08', 108),
  ('2024-07-09', 110),
  ('2024-07-10', 107),
  ('2024-07-11', 112),
  ('2024-07-12', 115);

SELECT COUNT(*) AS trading_days FROM W5D1_STOCK;

-- PART A: Window drills on the stock table

-- W1: Rank trading days by close price, highest first
SELECT
    trade_date,
    close_price,
    DENSE_RANK() OVER (ORDER BY close_price DESC) AS price_rank
FROM W5D1_STOCK
ORDER BY price_rank;

-- W2: Previous day's close and daily change
SELECT
    trade_date,
    close_price,
    LAG(close_price) OVER (ORDER BY trade_date) AS prev_close,
    close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change
FROM W5D1_STOCK
ORDER BY trade_date;

-- W3: Running maximum close and running average close over time
SELECT
    trade_date,
    close_price,
    MAX(close_price) OVER (ORDER BY trade_date) AS running_max_close,
    ROUND(AVG(close_price) OVER (ORDER BY trade_date), 2) AS running_avg_close
FROM W5D1_STOCK
ORDER BY trade_date;

-- W4: 3-day moving average of the close
SELECT
    trade_date,
    close_price,
    ROUND(AVG(close_price) OVER (
        ORDER BY trade_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3d
FROM W5D1_STOCK
ORDER BY trade_date;

-- W5: Which day(s) had the biggest single-day gain?
-- July 8, 2024 and July 11, 2024
WITH daily_changes AS (
    SELECT
        trade_date,
        close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change
    FROM W5D1_STOCK
)
SELECT trade_date, daily_change
FROM daily_changes
WHERE daily_change = (SELECT MAX(daily_change) FROM daily_changes);

-- W6: Combined query - all metrics in one result set
SELECT
    trade_date,
    close_price,
    LAG(close_price) OVER (ORDER BY trade_date) AS prev_close,
    close_price - LAG(close_price) OVER (ORDER BY trade_date) AS daily_change,
    ROUND(AVG(close_price) OVER (
        ORDER BY trade_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3d,
    MAX(close_price) OVER (ORDER BY trade_date) AS running_max_close,
    ROUND(AVG(close_price) OVER (ORDER BY trade_date), 2) AS running_avg_close,
    DENSE_RANK() OVER (ORDER BY close_price DESC) AS price_rank
FROM W5D1_STOCK
ORDER BY trade_date;

-- PART B: TPC-H stretch (window over an aggregate)

USE SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;

-- S1: Per order year - order count, total sales, and grand total on every row
SELECT
    YEAR(o_orderdate) AS order_year,
    COUNT(*) AS num_orders,
    SUM(o_totalprice) AS tot_sales,
    SUM(SUM(o_totalprice)) OVER () AS grand_total
FROM orders
GROUP BY order_year
ORDER BY order_year;

-- S2: Top 3 months by total sales within each year
WITH monthly_sales AS (
    SELECT
        YEAR(o_orderdate) AS order_year,
        MONTH(o_orderdate) AS order_month,
        COUNT(*) AS num_orders,
        SUM(o_totalprice) AS tot_sales
    FROM orders
    GROUP BY order_year, order_month
),
ranked AS (
    SELECT
        order_year,
        order_month,
        num_orders,
        tot_sales,
        RANK() OVER (PARTITION BY order_year ORDER BY tot_sales DESC) AS month_rank
    FROM monthly_sales
)
SELECT *
FROM ranked
WHERE month_rank <= 3
ORDER BY order_year, month_rank;
