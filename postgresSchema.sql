CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    cust VARCHAR(255),
    prod VARCHAR(255),
    state VARCHAR(255),
    date DATE,
    day INT,
    month INT,
    year INT,
    quant INT
);