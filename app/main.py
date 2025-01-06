from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.logger import logger

from app.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    NoUserIdException,
    NoUserException,
    NoJwtException,
)

from app.customers.router import router as router_customers
from app.products.router import router as router_products
from app.saledetails.router import router as router_saledetails
from app.sales.router import router as router_sales
from app.users.router import router_users, router_auth


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет мир API!"}


app.include_router(router_customers)
app.include_router(router_products)
app.include_router(router_sales)
app.include_router(router_saledetails)
app.include_router(router_users)
app.include_router(router_auth)


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(
    request: Request,
    exc: TokenExpiredException
):
    logger.error(exc)
    return RedirectResponse(url="/auth/")


@app.exception_handler(TokenNotFoundException)
async def token_not_found_exception_handler(
    request: Request,
    exc: TokenNotFoundException
):
    logger.error(exc)
    return RedirectResponse(url="/auth/")


@app.exception_handler(NoUserIdException)
async def no_user_id_exception_handler(
    request: Request,
    exc: NoUserIdException
):
    logger.error(exc)
    return RedirectResponse(url="/auth/")


@app.exception_handler(NoUserException)
async def no_user_exception_handler(
    request: Request,
    exc: NoUserException
):
    logger.error(exc)
    return RedirectResponse(url="/auth/")


@app.exception_handler(NoJwtException)
async def no_jwt_exception_handler(
    request: Request,
    exc: NoJwtException
):
    logger.error(exc)
    return RedirectResponse(url="/auth/")
