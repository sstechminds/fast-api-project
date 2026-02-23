import os

import duckdb
import httpx
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI  # noqa: UP035
from loguru import logger
from pydantic import BaseModel
from rich import print
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

load_dotenv()
api_key = os.getenv("API_KEY")

logger.info(f"API key is {api_key}")

app = FastAPI()


# Pydantic model for validation
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None  # Optional field with a default of None


@app.get("/")
async def root():
    logger.info("Info message")
    # asyncio.run(async_fetch_data('http://www.google.com'))
    results = await async_fetch_data("http://www.google.com")
    print("results: {results}".format(results=results))
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info("Info message")
    try:
        fetch_url("https://httpbin.org/status/500")  # Will trigger retries
        return {"message": "Hello World"}
    except Exception as e:
        print(f"Failed after retries: {e}")
    return {"message": f"Hello {name}"}


# Use the model as a type hint in a path operation
@app.post("/items/")
async def create_item(item: Item) -> dict[str, object]:
    # FastAPI validates the 'item' automatically
    model_dict = item.model_dump()
    logger.info(model_dict)
    df = pd.DataFrame([model_dict])
    logger.info(df.head())
    duckdb_df = duckdb.sql("SELECT name, price*2 AS double_price FROM df").df()  # in-memory query
    print(duckdb_df)
    return model_dict


# https://oneuptime.com/blog/post/2026-02-03-python-httpx-async-requests/view
async def async_fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:  # Async with Connection pool reused
        response = await client.get(url)
        # return response.json()
        return {"url": url, "status": response.status_code, "size": len(response.content)}


# Configure tenacity to retry on network errors, with exponential backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True,  # Reraise the last exception if all retries fail
)
def fetch_url(url: str) -> str:
    print(f"Attempting to fetch {url}...")
    response = httpx.get(url, timeout=5)
    # print(response.status_code)
    # print(response.json())  # User data dict
    # Raise an exception for 4xx or 5xx status codes to trigger retry
    response.raise_for_status()
    return response.text
