import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.market_data import get_real_time_quote
from fastapi import HTTPException

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.mark.anyio
async def test_get_quote_success():
    # Mock the response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "c": 150.00,
        "d": 1.50,
        "dp": 1.01,
        "h": 151.00,
        "l": 149.00,
        "o": 149.50,
        "pc": 148.50
    }
    
    # Mock the client context manager
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    
    # We need to mock the context manager __aenter__ and __aexit__
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("app.services.market_data.httpx.AsyncClient", return_value=mock_client):
        quote = await get_real_time_quote("AAPL")
        
        assert quote.symbol == "AAPL"
        assert quote.price == 150.00
        assert quote.change == 1.50
        assert quote.percent_change == 1.01

@pytest.mark.anyio
async def test_get_quote_invalid_symbol():
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Finnhub returns 0s for invalid symbols
    mock_response.json.return_value = {
        "c": 0,
        "d": 0,
        "dp": 0,
        "h": 0,
        "l": 0,
        "o": 0,
        "pc": 0
    }

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("app.services.market_data.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(HTTPException) as exc_info:
            await get_real_time_quote("INVALID")
        
        assert exc_info.value.status_code == 404

@pytest.mark.anyio
async def test_get_quote_api_failure():
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("app.services.market_data.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(HTTPException) as exc_info:
            await get_real_time_quote("AAPL")
        
        assert exc_info.value.status_code == 503

