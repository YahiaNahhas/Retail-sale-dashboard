DROP TABLE IF EXISTS retail_sales;

CREATE TABLE retail_sales (
  transactions_id INTEGER PRIMARY KEY,
  sale_date TEXT NOT NULL,
  sale_time TEXT NOT NULL,
  customer_id INTEGER NOT NULL,
  gender TEXT,
  age INTEGER,
  category TEXT NOT NULL,
  quantity INTEGER,
  price_per_unit REAL,
  cogs REAL,
  total_sale REAL
);
