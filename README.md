# Binance USDC Pair Price Fetcher

A Python tool to fetch cryptocurrency prices for USDC trading pairs from the Binance API.

## Features

- Fetch current price for any USDC trading pair
- Get detailed 24-hour statistics (high, low, volume, price change)
- List all available USDC trading pairs
- Retrieve prices for all USDC pairs at once
- No API key required (uses public endpoints)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

**Show help:**
```bash
python binance_usdc_prices.py
```

**List all available USDC pairs:**
```bash
python binance_usdc_prices.py list
```

**Get price for a specific pair:**
```bash
python binance_usdc_prices.py BTCUSDC
python binance_usdc_prices.py ETH    # Automatically adds USDC suffix
```

**Get detailed 24-hour statistics:**
```bash
python binance_usdc_prices.py BTCUSDC --full
```

**Get all USDC pair prices:**
```bash
python binance_usdc_prices.py all
```

### As a Python Module

```python
from binance_usdc_prices import BinanceUSDCPriceFetcher

# Initialize the fetcher
fetcher = BinanceUSDCPriceFetcher()

# Get a single price
price_data = fetcher.get_price('BTCUSDC')
print(f"BTC Price: {price_data['price']} USDC")

# Get 24-hour statistics
stats = fetcher.get_ticker_24h('ETHUSDC')
print(f"ETH 24h Change: {stats['priceChangePercent']}%")

# Get all USDC pairs
pairs = fetcher.get_all_usdc_pairs()
print(f"Available pairs: {pairs}")

# Get multiple prices
symbols = ['BTCUSDC', 'ETHUSDC', 'BNBUSDC']
prices = fetcher.get_multiple_prices(symbols)
for symbol, price in prices.items():
    print(f"{symbol}: {price}")

# Get all USDC prices at once
all_prices = fetcher.get_all_usdc_prices()
```

## API Methods

### `BinanceUSDCPriceFetcher` Class

- **`get_price(symbol)`** - Get current price for a specific symbol
- **`get_ticker_24h(symbol)`** - Get detailed 24-hour statistics
- **`get_all_usdc_pairs()`** - List all available USDC trading pairs
- **`get_multiple_prices(symbols)`** - Get prices for multiple symbols
- **`get_all_usdc_prices()`** - Get prices for all USDC pairs

## Response Format

### Simple Price Response
```json
{
  "symbol": "BTCUSDC",
  "price": "43250.50000000"
}
```

### 24-Hour Ticker Response
```json
{
  "symbol": "BTCUSDC",
  "priceChange": "1250.50000000",
  "priceChangePercent": "2.98",
  "lastPrice": "43250.50000000",
  "highPrice": "43500.00000000",
  "lowPrice": "41800.00000000",
  "volume": "12345.67800000"
}
```

## Examples

**Example 1: Monitor Bitcoin price**
```bash
python binance_usdc_prices.py BTCUSDC
```

Output:
```
Fetching price for BTCUSDC...
==================================================
BTCUSDC: 43,250.50000000 USDC
```

**Example 2: Get detailed Ethereum statistics**
```bash
python binance_usdc_prices.py ETHUSDC --full
```

Output:
```
Fetching detailed statistics for ETHUSDC...
==================================================

ETHUSDC:
  Current Price: 2,285.75000000 USDC
  24h Change: 45.25000000 (+2.02%)
  24h High: 2,310.00000000 USDC
  24h Low: 2,240.50000000 USDC
  24h Volume: 45,678.90
```

## Error Handling

The tool includes built-in error handling for:
- Network connection issues
- Invalid trading pairs
- API rate limits
- Invalid responses

Errors are printed to stdout with descriptive messages.

## Notes

- The Binance API has rate limits (typically 1200 requests per minute)
- All prices are in USDC
- The tool uses the public API endpoints (no authentication required)
- Prices are real-time from Binance exchange

## API Documentation

For more details on the Binance API, see: https://binance-docs.github.io/apidocs/spot/en/

## License

MIT License - Free to use and modify
