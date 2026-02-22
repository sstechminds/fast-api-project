from pprint import pprint

from fastapi import FastAPI # noqa: UP035
import httpx
from loguru import logger
from rich import print
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from pydantic import BaseModel

print("[bold green]Task completed successfully[/bold green]")

app = FastAPI()


@app.get("/")
async def root():
    logger.info("Info message")
    # asyncio.run(async_fetch_data('http://www.google.com'))
    results = await async_fetch_data('http://www.google.com')
    pprint('results: {results}'.format(results=results))
    return {"message": f"Hello world!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info("Info message")
    try:
        data = fetch_url("https://httpbin.org/status/500")  # Will trigger retries
        return {"message": "Hello World"}
    except Exception as e:
        print(f"Failed after retries: {e}")
    return {"message": f"Hello {name}"}


# Pydantic model for validation
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None # Optional field with a default of None


# Use the model as a type hint in a path operation
@app.post("/items/")
async def create_item(item: Item):
    # FastAPI validates the 'item' automatically
    return {"item_name": item.name, "item_price": item.price}


# https://oneuptime.com/blog/post/2026-02-03-python-httpx-async-requests/view
async def async_fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client: # Async with Connection pool reused
        response = await client.get(url)
        # return response.json()
        return {
            "url": url,
            "status": response.status_code,
            "size": len(response.content)
        }


# Configure tenacity to retry on network errors, with exponential backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True # Reraise the last exception if all retries fail
)
def fetch_url(url: str) -> str:
    print(f"Attempting to fetch {url}...")
    response = httpx.get(url, timeout=5)
    # print(response.status_code)
    # print(response.json())  # User data dict
    # Raise an exception for 4xx or 5xx status codes to trigger retry
    response.raise_for_status()
    return response.text
