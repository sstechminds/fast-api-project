import pytest
from httpx import AsyncClient, ASGITransport # Import ASGITransport
from unittest.mock import patch, MagicMock

from main import app

# Wrap the app in ASGITransport
transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_root_success():
    """Tests the / route by mocking the async_fetch_data function."""
    # We patch the fetch function where it is imported/used in your app
    with patch("main.async_fetch_data") as mocked_fetch:
        # Define what the mock should return
        mocked_fetch.return_value = "Mocked Google Content"

        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
            response = await ac.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello world!"}
        mocked_fetch.assert_called_once_with('http://www.google.com')


@pytest.mark.asyncio
async def test_say_hello_exception_handling():
    """Tests /hello/{name} when the external fetch fails."""
    with patch("main.fetch_url") as mocked_fetch_url:
        # Simulate an exception being raised by the external utility
        mocked_fetch_url.side_effect = Exception("Connection Failed")

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/hello/Gemini")

        assert response.status_code == 200
        # Even though fetch failed, your code catches the exception
        # and returns the fallback message
        assert response.json() == {"message": "Hello Gemini"}
        mocked_fetch_url.assert_called_once()


@pytest.mark.asyncio
async def test_say_hello_success():
    """Tests /hello/{name} when the external fetch succeeds."""
    with patch("main.fetch_url") as mocked_fetch_url:
        mocked_fetch_url.return_value = {"status": "success"}

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/hello/World")

        assert response.status_code == 200
        # Based on your logic, if it succeeds, it returns "Hello World"
        assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_create_item_success():
    """Tests the /items/ POST endpoint with valid item data."""
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(
            "/items/",
            json={"name": "Widget", "price": 1.0}
        )

    assert response.status_code == 200
    assert response.json() == {
        "item_name": "Widget",
        "item_price": 1.0
    }


@pytest.mark.asyncio
async def test_create_item_invalid_price_type():
    """Tests the /items/ POST endpoint with invalid price type."""
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(
            "/items/",
            json={"name": "Widget", "price": "invalid"}
        )

    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()