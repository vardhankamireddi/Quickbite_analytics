-- ============================================================
-- QuickBite Analytics – Script 02: Create Tables
-- Team: Data Knights | CODEGNAN DA-07
-- MySQL 8.0+ Compatible
-- ============================================================

USE quickbite_analytics;

-- ─────────────────────────────────────────
-- 1. RIDERS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS riders (
    rider_id            VARCHAR(10)  NOT NULL,
    rider_city          VARCHAR(50)  NOT NULL,
    availability_status VARCHAR(20)  NOT NULL DEFAULT 'Active',

    CONSTRAINT pk_riders PRIMARY KEY (rider_id),
    CONSTRAINT chk_rider_status CHECK (
        availability_status IN ('Active', 'Inactive', 'On Leave')
    )
);

CREATE INDEX idx_riders_city ON riders (rider_city);
CREATE INDEX idx_riders_status ON riders (availability_status);

-- ─────────────────────────────────────────
-- 2. CUSTOMERS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customers (
    customer_id   VARCHAR(10)  NOT NULL,
    signup_date   DATE         NOT NULL,
    city          VARCHAR(50)  NOT NULL,
    total_orders  INT          NOT NULL DEFAULT 0,

    CONSTRAINT pk_customers PRIMARY KEY (customer_id),
    CONSTRAINT chk_customer_city CHECK (
        city IN ('Hyderabad', 'Visakhapatnam', 'Vijayawada')
    ),
    CONSTRAINT chk_total_orders CHECK (total_orders >= 0)
);

CREATE INDEX idx_customers_city ON customers (city);
CREATE INDEX idx_customers_signup ON customers (signup_date);

-- ─────────────────────────────────────────
-- 3. RESTAURANTS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id     VARCHAR(10)   NOT NULL,
    restaurant_name   VARCHAR(150)  NOT NULL,
    cuisine           VARCHAR(50)   NOT NULL,
    area              VARCHAR(80)   NOT NULL,
    city              VARCHAR(50)   NOT NULL,
    avg_prep_time     DECIMAL(5,1)  NOT NULL COMMENT 'Average preparation time in minutes',
    restaurant_rating DECIMAL(3,1)  NOT NULL,

    CONSTRAINT pk_restaurants PRIMARY KEY (restaurant_id),
    CONSTRAINT chk_rest_city CHECK (
        city IN ('Hyderabad', 'Visakhapatnam', 'Vijayawada')
    ),
    CONSTRAINT chk_rest_rating CHECK (
        restaurant_rating >= 1.0 AND restaurant_rating <= 5.0
    ),
    CONSTRAINT chk_prep_time CHECK (avg_prep_time > 0)
);

CREATE INDEX idx_rest_city ON restaurants (city);
CREATE INDEX idx_rest_cuisine ON restaurants (cuisine);
CREATE INDEX idx_rest_area ON restaurants (area);
CREATE INDEX idx_rest_rating ON restaurants (restaurant_rating);

-- ─────────────────────────────────────────
-- 4. ORDERS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    order_id             VARCHAR(12)    NOT NULL,
    customer_id          VARCHAR(10)    NOT NULL,
    restaurant_id        VARCHAR(10)    NOT NULL,
    rider_id             VARCHAR(10)    NOT NULL,
    order_time           DATETIME       NOT NULL,
    order_value          DECIMAL(10,2)  NOT NULL COMMENT 'Gross order value in INR',
    discount             DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    final_amount         DECIMAL(10,2)  NOT NULL COMMENT 'Net amount after discount',
    order_status         VARCHAR(30)    NOT NULL,
    cancellation_reason  VARCHAR(100)   NULL DEFAULT NULL,

    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id),
    CONSTRAINT fk_orders_restaurant  FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    CONSTRAINT fk_orders_rider       FOREIGN KEY (rider_id)      REFERENCES riders(rider_id),
    CONSTRAINT chk_order_status CHECK (
        order_status IN ('Completed', 'Cancelled', 'Refunded', 'Partially Delivered')
    ),
    CONSTRAINT chk_order_value  CHECK (order_value  > 0),
    CONSTRAINT chk_discount     CHECK (discount     >= 0),
    CONSTRAINT chk_final_amount CHECK (final_amount >= 0)
);

CREATE INDEX idx_orders_customer    ON orders (customer_id);
CREATE INDEX idx_orders_restaurant  ON orders (restaurant_id);
CREATE INDEX idx_orders_rider       ON orders (rider_id);
CREATE INDEX idx_orders_time        ON orders (order_time);
CREATE INDEX idx_orders_status      ON orders (order_status);
CREATE INDEX idx_orders_hour        ON orders ((HOUR(order_time)));
CREATE INDEX idx_orders_date        ON orders ((DATE(order_time)));

-- ─────────────────────────────────────────
-- 5. DELIVERIES
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id              VARCHAR(12)   NOT NULL,
    order_id                 VARCHAR(12)   NOT NULL,
    rider_id                 VARCHAR(10)   NOT NULL,
    pickup_time              DATETIME      NOT NULL,
    delivery_time            DATETIME      NOT NULL,
    distance_km              DECIMAL(6,2)  NOT NULL COMMENT 'Road distance in km',
    estimated_delivery_time  DECIMAL(6,1)  NOT NULL COMMENT 'Estimated total delivery time in minutes',
    actual_delivery_minutes  DECIMAL(6,1)  NOT NULL COMMENT 'Actual delivery time in minutes',
    delay_minutes            DECIMAL(6,1)  NOT NULL COMMENT 'Positive = delayed, Negative = early',
    on_time_status           VARCHAR(10)   NOT NULL,

    CONSTRAINT pk_deliveries PRIMARY KEY (delivery_id),
    CONSTRAINT uq_deliveries_order UNIQUE (order_id),        -- one delivery per order
    CONSTRAINT fk_deliveries_order FOREIGN KEY (order_id)  REFERENCES orders(order_id),
    CONSTRAINT fk_deliveries_rider FOREIGN KEY (rider_id)  REFERENCES riders(rider_id),
    CONSTRAINT chk_on_time_status CHECK (
        on_time_status IN ('On Time', 'Delayed')
    ),
    CONSTRAINT chk_distance CHECK (distance_km > 0),
    CONSTRAINT chk_actual_del CHECK (actual_delivery_minutes > 0),
    CONSTRAINT chk_delivery_after_pickup CHECK (delivery_time > pickup_time)
);

CREATE INDEX idx_del_order  ON deliveries (order_id);
CREATE INDEX idx_del_rider  ON deliveries (rider_id);
CREATE INDEX idx_del_status ON deliveries (on_time_status);
CREATE INDEX idx_del_delay  ON deliveries (delay_minutes);

-- ─────────────────────────────────────────
-- 6. FEEDBACK
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id     VARCHAR(12)    NOT NULL,
    order_id        VARCHAR(12)    NOT NULL,
    customer_id     VARCHAR(10)    NOT NULL,
    rating          TINYINT        NOT NULL COMMENT '1–5 stars',
    review_text     VARCHAR(300)   NULL,
    complaint_type  VARCHAR(50)    NULL DEFAULT NULL,
    refund_amount   DECIMAL(10,2)  NOT NULL DEFAULT 0.00,

    CONSTRAINT pk_feedback PRIMARY KEY (feedback_id),
    CONSTRAINT uq_feedback_order UNIQUE (order_id),          -- one feedback per order
    CONSTRAINT fk_feedback_order    FOREIGN KEY (order_id)    REFERENCES orders(order_id),
    CONSTRAINT fk_feedback_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT chk_refund CHECK (refund_amount >= 0)
);

CREATE INDEX idx_fb_order    ON feedback (order_id);
CREATE INDEX idx_fb_customer ON feedback (customer_id);
CREATE INDEX idx_fb_rating   ON feedback (rating);

-- ─────────────────────────────────────────
-- Verify table creation
-- ─────────────────────────────────────────
SELECT
    TABLE_NAME,
    TABLE_ROWS,
    CREATE_TIME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'quickbite_analytics'
ORDER BY TABLE_NAME;
