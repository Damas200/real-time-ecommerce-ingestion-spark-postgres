-- ============================================
-- PostgreSQL Setup Script
-- Project: Real-Time E-Commerce Event Ingestion
-- ============================================

-- Create database
CREATE DATABASE spark_db;

-- Connect to database
\c spark_db;

-- Drop table if it already exists (for clean re-runs)
DROP TABLE IF EXISTS user_events;

-- Create table for streaming events
CREATE TABLE user_events (
    event_id UUID PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    price DECIMAL(10,2),
    event_timestamp TIMESTAMP NOT NULL,
    event_hour INT
);

-- Indexes for performance
CREATE INDEX idx_event_timestamp ON user_events(event_timestamp);
CREATE INDEX idx_event_type ON user_events(event_type);

-- Verification
SELECT 'Table user_events created successfully' AS status;
