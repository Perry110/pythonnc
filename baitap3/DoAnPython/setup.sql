

-- Sử dụng cơ sở dữ liệu 'logindb'
\c logindb;

CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    name VARCHAR(255),
    price NUMERIC(10, 2),
    quantity INTEGER DEFAULT 1
);

