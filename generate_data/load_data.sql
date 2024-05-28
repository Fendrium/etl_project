-- COMPANIES
DROP TABLE IF EXISTS companies, products, customers, prices, orders CASCADE;

CREATE TABLE companies (
  company_id INT PRIMARY KEY,
  cuit_no INT,
  name TEXT,
  is_supplier BOOL
);
COPY companies 
FROM '/usr/lib/generate_data/companies.csv'
DELIMITER ',' CSV HEADER;

-- PRODUCTS
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  supplier_id INT,
  name TEXT,
  default_price INT,
  CONSTRAINT fk_supplier
    FOREIGN KEY(supplier_id) 
	  REFERENCES companies(company_id)
	  ON DELETE SET NULL
);
COPY products 
FROM '/usr/lib/generate_data/products.csv'
DELIMITER ',' CSV HEADER;

-- CUSTOMERS
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  document_no INT,
  name TEXT,
  date_of_birth DATE
);
COPY customers
FROM '/usr/lib/generate_data/customers.csv'
DELIMITER ',' CSV HEADER;

-- PRICES
CREATE TABLE prices (
  price_id INT PRIMARY KEY,
  company_id INT REFERENCES companies(company_id),
  product_id INT REFERENCES products(product_id),
  supplier_id INT REFERENCES companies(company_id),
  price INT
);
COPY prices 
FROM '/usr/lib/generate_data/prices.csv'
DELIMITER ',' CSV HEADER;

-- ORDERS
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  order_date DATE,
  company_id INT REFERENCES companies(company_id),
  customer_id INT REFERENCES customers(customer_id),
  product_id INT REFERENCES products(product_id),
  units INT
  );
COPY orders 
FROM '/usr/lib/generate_data/orders.csv'
DELIMITER ',' CSV HEADER;
