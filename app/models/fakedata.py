from os.path import abspath, dirname, join
import sys

sys.path.append(abspath(join(dirname(__file__), "../../")))

from app.database import async_session_maker
from app.customers.models import Customer
from app.products.models import Product 
from app.sales.models import Sale
from app.saledetails.models import SaleDetails 

from faker import Faker
import random
import asyncio

from sqlalchemy import text

fake = Faker()

def generate_random_customer(num_records=1):
    customers = []
    emails = []
    for _ in range(num_records):
        email_new = fake.email()
        if email_new not in emails:
            emails.append(email_new)
            customer = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
                'email': email_new,
                'phone_number': fake.phone_number(),
                'gender': random.choice(['Male', 'Female']),
            }
            customers.append(customer)
    return customers

def generate_random_product(num_records=1):
    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Groceries']
    products = []
    for _ in range(num_records):
        product = {
            'product_name': fake.word(),
            'product_description': fake.text(),
            'product_category': random.choice(categories),
            'unit_price': round(random.uniform(5.0, 500.0), 2),
        }
        products.append(product)
    return products

def generate_random_sales_and_details(num_records, customer_ids, product_ids):
    sales = []
    sale_details = []
    sale_id_counter = 1 

    for _ in range(num_records):
        sale_id = sale_id_counter 
        sale_id_counter += 1
        customer_id = random.choice(customer_ids)
        sale_date = fake.date_this_year()

        sales.append({
            'sale_id': sale_id,
            'branch': fake.city(),
            'city': fake.city(),
            'customer_type': random.choice(['Member', 'Normal']),
            'customer_id': customer_id,
            'sale_date': sale_date,
        })

        added_details = set()

        for _ in range(random.randint(1, 5)):
            product_id = random.choice(product_ids)
            if (sale_id, product_id) not in added_details:
                sale_details.append({
                    'sale_id': sale_id,
                    'product_id': product_id,
                    'quantity': random.randint(1, 10),
                })
                added_details.add((sale_id, product_id))

    return sales, sale_details

async def insert_customers(customers):
    async with async_session_maker() as session:
        for customer in customers:
            new_customer = Customer(**customer)
            session.add(new_customer)
        await session.commit()

async def insert_products(products):
    async with async_session_maker() as session:
        for product in products:
            new_product = Product(**product)
            session.add(new_product)
        await session.commit()

async def insert_sales(sales):
    async with async_session_maker() as session:
        for sale in sales:
            new_sale = Sale(**sale)
            session.add(new_sale)
        await session.commit()

async def insert_sale_details(sale_details):
    async with async_session_maker() as session:
        for detail in sale_details:
            new_detail = SaleDetails(**detail)
            session.add(new_detail)
        await session.commit()

async def get_customers():
    async with async_session_maker() as session:
        result = await session.execute(text("SELECT customer_id FROM customers"))
        return [row[0] for row in result.fetchall()]

async def get_products():
    async with async_session_maker() as session:
        result = await session.execute(text("SELECT product_id FROM products"))
        return [row[0] for row in result.fetchall()]


async def main():
    customers = generate_random_customer(1000)
    await insert_customers(customers)

    products = generate_random_product(1000)
    await insert_products(products)

    customers = await get_customers()
    products = await get_products()

    sales, sale_details = generate_random_sales_and_details(1000, customers, products)  # Генерируем продажи и детали
    await insert_sales(sales)
    await insert_sale_details(sale_details)

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())