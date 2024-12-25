from fastapi import FastAPI
from app.customers.router import router as router_customers
from app.products.router import router as router_products
from app.saledetails.router import router as router_saledetails
from app.sales.router import router as router_sales

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет мир API!"}


app.include_router(router_customers)
app.include_router(router_products)
app.include_router(router_sales)
app.include_router(router_saledetails)