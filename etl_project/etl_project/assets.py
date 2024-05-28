from dagster import (
    asset,
)
import polars as pl
import psycopg2


def connect_to_db():
    conn = psycopg2.connect(
        host="postgres_b2b_platform",
        database="b2b_db",
        user="b2b_user",
        password="P4ssw0rd&!",
    )
    cursor = conn.cursor()
    return cursor


def connect_to_dwh():
    conn = psycopg2.connect(
        host="postgres_dwh",
        port=5432,
        database="dwh_db",
        user="dwh_user",
        password="P4ssw0rd&!",
    )
    cursor = conn.cursor()
    return cursor


def map_dict(cols_in, cols_out):
    return {col_in: cols_out[i] for i, col_in in enumerate(cols_in)}


@asset
def orders():
    cursor = connect_to_db()
    cursor.execute("SELECT * from orders")
    rows = cursor.fetchall()
    order_cols = [
        "order_id",
        "order_date",
        "company_id",
        "customer_id",
        "product_id",
        "units",
    ]
    order_df = pl.DataFrame(rows)
    order_df = order_df.rename(map_dict(order_df.columns, order_cols))
    order_df.write_csv("orders.csv", include_header=True)
    cursor.close()


@asset
def companies():
    cursor = connect_to_db()
    cursor.execute("SELECT * from companies")
    rows = cursor.fetchall()
    company_cols = ["company_id", "cuit_no", "company_name", "is_supplier"]
    company_df = pl.DataFrame(rows)
    company_df = company_df.rename(map_dict(company_df.columns, company_cols))
    company_df.write_csv("companies.csv", include_header=True)
    cursor.close()


@asset
def customers():
    cursor = connect_to_db()
    cursor.execute("SELECT * from customers")
    rows = cursor.fetchall()
    customer_cols = ["customer_id", "document_no", "customer_name", "date_of_birth"]
    customer_df = pl.DataFrame(rows)
    customer_df = customer_df.rename(map_dict(customer_df.columns, customer_cols))
    customer_df.write_csv("customers.csv", include_header=True)
    cursor.close()


@asset
def prices():
    cursor = connect_to_db()
    cursor.execute("SELECT * from prices")
    rows = cursor.fetchall()
    price_cols = ["id", "company_id", "product_id", "supplier_id", "price"]
    price_df = pl.DataFrame(rows)
    price_df = price_df.transpose()
    price_df = price_df.rename(map_dict(price_df.columns, price_cols))
    price_df.write_csv("prices.csv", include_header=True)
    cursor.close()


@asset
def products():
    cursor = connect_to_db()
    cursor.execute("SELECT * from products")
    rows = cursor.fetchall()
    product_cols = ["product_id", "supplier_id", "product_name", "default_price"]
    product_df = pl.DataFrame(rows)
    product_df = product_df.rename(map_dict(product_df.columns, product_cols))
    product_df.write_csv("products.csv", include_header=True)
    cursor.close()


@asset(deps=[orders, prices, customers, companies, products])
def order_denormalized():
    orders = pl.read_csv("./orders.csv", has_header=True)
    customers = pl.read_csv("./customers.csv", has_header=True)
    companies = pl.read_csv("./companies.csv", has_header=True)
    products = pl.read_csv("./products.csv", has_header=True)

    orders = orders.join(companies, on="company_id", how="left")
    orders = orders.join(customers, on="customer_id", how="left")
    orders = orders.join(products, on="product_id", how="left")
    print(orders.columns)
    orders.write_csv("orders_denorm.csv")


@asset(deps=[order_denormalized])
def load_data():
    orders = pl.read_csv("./orders_denorm.csv", has_header=True)
    orders.write_database(
        table_name="orders",
        connection="postgresql://dwh_user:P4ssw0rd&!@postgres_dwh:5432/dwh_db",
        if_table_exists="replace",
        engine="adbc",
        engine_options={"temporary": True},
    )
