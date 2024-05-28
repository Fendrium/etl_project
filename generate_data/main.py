from faker import Faker
import pandas as pd
from faker.providers import DynamicProvider
import faker_commerce

# Generate "realistic" data (children data use parent data)


fake = Faker()
fake.add_provider(faker_commerce.Provider)
# Companies
companies = []
for i in range(0, 50):
    companies.append(
        [
            i,
            str(fake.unique.random_int(min=111111, max=999999)),
            fake.company(),
            fake.boolean(),
        ]
    )

companies_df = pd.DataFrame(companies, columns=["id", "cuit_no", "name", "is_supplier"])

supplier_df = companies_df.loc[companies_df["is_supplier"]]
supplier_list = list(supplier_df["id"])
company_list = list(companies_df["id"])

company_provider = DynamicProvider(
    provider_name="company_provider", elements=company_list
)
supplier_provider = DynamicProvider(
    provider_name="supplier_provider", elements=supplier_list
)


fake.add_provider(company_provider)
fake.add_provider(supplier_provider)

# Customers
customers = []
for i in range(0, 200):
    customers.append(
        [
            i,
            str(fake.unique.random_int(min=111111, max=999999)),
            fake.name(),
            fake.date_of_birth(),
        ]
    )

customers_df = pd.DataFrame(
    customers, columns=["id", "document_no", "name", "date_of_birth"]
)

customer_list = list(customers_df["id"])
customer_provider = DynamicProvider(
    provider_name="customer_provider", elements=customer_list
)
fake.add_provider(customer_provider)

# Products
products = []
for i in range(0, 1000):
    products.append(
        [
            i,
            fake.supplier_provider(),
            fake.ecommerce_name(),
            fake.random_int(min=1, max=150),
        ]
    )
products_df = pd.DataFrame(
    products, columns=["id", "supplier_id", "name", "default_price"]
)

product_list = list(products_df["id"])

product_provider = DynamicProvider(
    provider_name="product_provider", elements=product_list
)
fake.add_provider(product_provider)

# Prices
prices = []
for i in range(0, 1000):
    prices.append(
        [
            i,
            fake.company_provider(),
            fake.product_provider(),
            fake.supplier_provider(),
            fake.random_int(min=1, max=150),
        ]
    )


prices_df = pd.DataFrame(
    prices, columns=["id", "company_id", "product_id", "supplier_id", "price"]
)
print(prices_df)

# Orders
orders = []
for i in range(0, 10000):
    orders.append(
        [
            i,
            fake.date_this_year(),
            fake.company_provider(),
            fake.customer_provider(),
            fake.product_provider(),
            fake.random_int(min=1, max=50),
        ]
    )
orders_df = pd.DataFrame(
    orders,
    columns=["id", "order_date", "company_id", "customer_id", "product_id", "units"],
)

output_folder = "."

companies_df.to_csv(f"{output_folder}/companies.csv", index=False)
products_df.to_csv(f"{output_folder}/products.csv", index=False)
prices_df.to_csv(f"{output_folder}/prices.csv", index=False)
customers_df.to_csv(f"{output_folder}/customers.csv", index=False)
orders_df.to_csv(f"{output_folder}/orders.csv", index=False)
