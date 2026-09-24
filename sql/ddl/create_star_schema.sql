-- ============================================================================
-- CLOUDMART ANALYTICS - REDSHIFT STAR SCHEMA DDL
-- Database: cloudmart_dw
-- Schema: public / analytics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DIMENSION: dim_customer (SCD Type 2)
-- Grain: One row per customer version.
-- Logic: Maintains historical tracking of customer address, tier, and region.
--        `effective_date` & `end_date` define valid time boundary.
--        `is_current` = TRUE identifies active profile.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key        BIGINT IDENTITY(1,1) PRIMARY KEY, -- Surrogate Key
    customer_id         VARCHAR(64) NOT NULL,              -- Business/Natural Key
    first_name          VARCHAR(100),
    last_name           VARCHAR(100),
    email               VARCHAR(255),
    customer_segment    VARCHAR(50),                       -- Tier: VIP, Standard, Premium
    country             VARCHAR(100),
    city                VARCHAR(100),
    postal_code         VARCHAR(20),
    effective_date      DATE NOT NULL,                     -- SCD2 Start Date
    end_date            DATE DEFAULT '9999-12-31',         -- SCD2 End Date
    is_current          BOOLEAN DEFAULT TRUE,              -- SCD2 Active Flag
    version             INT DEFAULT 1                      -- Record Version Number
)
DISTSTYLE KEY
DISTKEY (customer_id)
COMPOUND SORTKEY (customer_id, is_current);

COMMENT ON TABLE dim_customer IS 'SCD Type 2 Customer Dimension tracking demographic and tier changes over time.';


-- ----------------------------------------------------------------------------
-- 2. DIMENSION: dim_product (SCD Type 2)
-- Grain: One row per product version.
-- Logic: Maintains historical price adjustments, categories, and brand tags.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_product (
    product_key         BIGINT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate Key
    product_id          VARCHAR(64) NOT NULL,               -- Business/Natural Key
    product_name        VARCHAR(255) NOT NULL,
    category            VARCHAR(100),
    subcategory         VARCHAR(100),
    brand               VARCHAR(100),
    unit_cost           DECIMAL(10,2),
    list_price          DECIMAL(10,2),
    effective_date      DATE NOT NULL,
    end_date            DATE DEFAULT '9999-12-31',
    is_current          BOOLEAN DEFAULT TRUE,
    version             INT DEFAULT 1
)
DISTSTYLE ALL
COMPOUND SORTKEY (category, product_id);

COMMENT ON TABLE dim_product IS 'SCD Type 2 Product Dimension capturing price changes and re-categorizations.';


-- ----------------------------------------------------------------------------
-- 3. DIMENSION: dim_date
-- Grain: One row per calendar date.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_date (
    date_key            INT PRIMARY KEY,                   -- YYYYMMDD integer key
    full_date           DATE UNIQUE NOT NULL,
    day_of_week         INT,
    day_name            VARCHAR(20),
    day_of_month        INT,
    day_of_year         INT,
    week_of_year        INT,
    month_number        INT,
    month_name          VARCHAR(20),
    quarter             INT,
    year                INT,
    is_weekend          BOOLEAN
)
DISTSTYLE ALL
SORTKEY (date_key);

COMMENT ON TABLE dim_date IS 'Standard Date Dimension for calendar hierarchy rollups.';


-- ----------------------------------------------------------------------------
-- 4. DIMENSION: dim_region
-- Grain: One row per sales region/territory.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_region (
    region_key          INT IDENTITY(1,1) PRIMARY KEY,
    region_id           VARCHAR(32) UNIQUE NOT NULL,
    region_name         VARCHAR(100) NOT NULL,              -- North America, EMEA, APAC, LATAM
    country_code        VARCHAR(10),
    manager_name        VARCHAR(100)
)
DISTSTYLE ALL;

COMMENT ON TABLE dim_region IS 'Geographic region and territory hierarchy dimension.';


-- ----------------------------------------------------------------------------
-- 5. FACT: fact_sales
-- Grain: One row per completed line item order transaction.
-- Foreign Keys link to active surrogate keys in dimensions at order time.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_fact_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id            VARCHAR(64) NOT NULL,
    order_line_number   INT NOT NULL,
    customer_key        BIGINT REFERENCES dim_customer(customer_key),
    product_key         BIGINT REFERENCES dim_product(product_key),
    date_key            INT REFERENCES dim_date(date_key),
    region_key          INT REFERENCES dim_region(region_key),
    order_timestamp     TIMESTAMP NOT NULL,
    quantity            INT NOT NULL,
    unit_price          DECIMAL(10,2) NOT NULL,
    discount_amount     DECIMAL(10,2) DEFAULT 0.00,
    gross_amount        DECIMAL(10,2) NOT NULL,
    net_amount          DECIMAL(10,2) NOT NULL,
    payment_method      VARCHAR(50)
)
DISTSTYLE KEY
DISTKEY (customer_key)
COMPOUND SORTKEY (date_key, product_key);

COMMENT ON TABLE fact_sales IS 'Central sales transaction fact table measuring revenue metrics at order line item grain.';
