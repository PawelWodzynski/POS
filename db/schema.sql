-- Initialization schema for POS project (no migrations)
-- Tables designed to work with products coming from FakeStoreAPI.
-- This file was moved into db/ to be used by docker-compose initialization.
-- Run with: psql "postgresql://user:pass@host:port/dbname" -f schema.sql
-- or via your preferred Postgres client.

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert default roles
INSERT INTO roles (id, name) VALUES
    (1, 'ADMIN')
ON CONFLICT (id) DO NOTHING;

INSERT INTO roles (id, name) VALUES
    (2, 'CUSTOMER')
ON CONFLICT (id) DO NOTHING;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- store hashed password
    email VARCHAR(255) NOT NULL UNIQUE,
    city VARCHAR(150),
    street VARCHAR(255),
    postal_code VARCHAR(30),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role_id INTEGER NOT NULL DEFAULT 2 REFERENCES roles(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Orders table
-- product_json stores the full product object retrieved from FakeStoreAPI (JSONB)
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    product_json JSONB NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
-- GIN index to speed JSON queries on product_json
CREATE INDEX IF NOT EXISTS idx_orders_product_json_gin ON orders USING gin (product_json);

-- Insert default admin user with ADMIN role
INSERT INTO customers (login, password, email, role_id, created_at)
VALUES (
    'admin',
    '$2a$12$/4jQc5UJNkfqQkb3qJEWtOt4C0C45FSue3z0dAfYFETjQCi6Uqy/i',
    'admin@example.com',
    1,
    now()
)
ON CONFLICT (login) DO NOTHING;
