-- Week 4 Day 2: Snowflake SQL transfer drills
-- Work in your copy under student-work/week4/day2/.
-- Replace the warehouse placeholder before running the setup commands.
-- Query the shared sample data only. Do not create or change objects.

USE WAREHOUSE <INSTRUCTOR_WAREHOUSE>;
USE DATABASE SNOWFLAKE_SAMPLE_DATA;
USE SCHEMA TPCH_SF1;

-- Confirm that TPCH_SF1 is the current schema before starting.
SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();

-- ============================================================
-- TIER A: FOUNDATION
-- ============================================================

-- DRILL 1: Customers from one nation
-- Table: CUSTOMER
-- Output grain: one customer
-- TODO: Write the query described in the activity handout.


-- DRILL 2: Suppliers with strong account balances
-- Table: SUPPLIER
-- Output grain: one supplier
-- TODO: Write the query described in the activity handout.


-- DRILL 3: Categorize part sizes
-- Table: PART
-- Output grain: one part
-- TODO: Write the query described in the activity handout.


-- DRILL 4: Order count by year
-- Table: ORDERS
-- Output grain: one calendar year
-- TODO: Write the query described in the activity handout.


-- DRILL 5: Order status summary
-- Table: ORDERS
-- Output grain: one order status
-- TODO: Write the query described in the activity handout.


-- ============================================================
-- TIER B: RELATIONSHIPS
-- ============================================================

-- DRILL 6: High-volume order clerks
-- Table: ORDERS
-- Output grain: one clerk
-- TODO: Write the query described in the activity handout.


-- DRILL 7: German customer directory
-- Tables: CUSTOMER, NATION
-- Output grain: one customer
-- TODO: Write the query described in the activity handout.


-- DRILL 8: Market segment order performance
-- Tables: CUSTOMER, ORDERS
-- Output grain: one customer market segment
-- TODO: Write the query described in the activity handout.


-- DRILL 9: Supplier count by region
-- Tables: REGION, NATION, SUPPLIER
-- Output grain: one region
-- TODO: Write the query described in the activity handout.


-- DRILL 10: Top German customers
-- Tables: CUSTOMER, ORDERS, NATION
-- Output grain: one customer
-- TODO: Write the query described in the activity handout.


-- ============================================================
-- TIER C: CHALLENGE
-- ============================================================

-- DRILL 11: Parts supplied from Europe
-- Tables: PART, PARTSUPP, SUPPLIER, NATION, REGION
-- Output grain: one part and supplier relationship
-- TODO: Write the query described in the activity handout.


-- DRILL 12: Orders containing part 5
-- Tables: CUSTOMER, ORDERS, LINEITEM
-- Output grain: one qualifying order
-- TODO: Write the query described in the activity handout.


-- DRILL 13: Delayed shipment lines
-- Tables: ORDERS, LINEITEM
-- Output grain: one order line
-- TODO: Write the query described in the activity handout.


-- ============================================================
-- TIER D: INTERMEDIATE EXTENSION
-- ============================================================

-- DRILL 14: Orders with many line items
-- Table: LINEITEM
-- Output grain: one order
-- TODO: Write the query described in the activity handout.


-- DRILL 15: Top suppliers by discounted revenue
-- Tables: SUPPLIER, LINEITEM
-- Output grain: one supplier
-- TODO: Write the query described in the activity handout.


-- ============================================================
-- REFLECTION
-- ============================================================

-- 1. One SQL pattern that worked the same way across platforms:
--

-- 2. One Snowflake session command that was platform-specific:
--

-- 3. One validation check that changed or confirmed your interpretation:
--
