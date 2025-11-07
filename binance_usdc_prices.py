#!/usr/bin/env python3
"""
Binance USDC Pair Price Fetcher

This tool fetches current prices for cryptocurrency pairs with USDC from Binance.
Uses the Binance public API - no authentication required.
"""

import requests
import json
from typing import Dict, List, Optional
import sys


class BinanceUSDCPriceFetcher:
    """Fetch USDC pair prices from Binance API"""
    
    BASE_URL = "https://api.binance.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        
    def get_all_usdc_pairs(self) -> List[str]:
        """Get all available USDC trading pairs"""
        try:
            response = self.session.get(f"{self.BASE_URL}/exchangeInfo")
            response.raise_for_status()
            data = response.json()
            
            usdc_pairs = [
                symbol['symbol'] 
                for symbol in data['symbols'] 
                if symbol['symbol'].endswith('USDC') and symbol['status'] == 'TRADING'
            ]
            return sorted(usdc_pairs)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trading pairs: {e}")
            return []
    
    def get_price(self, symbol: str) -> Optional[Dict]:
        """
        Get current price for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDC', 'ETHUSDC')
            
        Returns:
            Dictionary with price information or None if error
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/ticker/price",
                params={'symbol': symbol}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_ticker_24h(self, symbol: str) -> Optional[Dict]:
        """
        Get 24-hour ticker statistics for a symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDC', 'ETHUSDC')
            
        Returns:
            Dictionary with 24h statistics or None if error
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/ticker/24hr",
                params={'symbol': symbol}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching 24h ticker for {symbol}: {e}")
            return None
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Optional[str]]:
        """
        Get prices for multiple symbols
        
        Args:
            symbols: List of trading pair symbols
            
        Returns:
            Dictionary mapping symbols to their prices
        """
        prices = {}
        for symbol in symbols:
            price_data = self.get_price(symbol)
            if price_data:
                prices[symbol] = price_data['price']
            else:
                prices[symbol] = None
        return prices
    
    def get_all_usdc_prices(self) -> Dict[str, str]:
        """Get prices for all USDC pairs"""
        try:
            response = self.session.get(f"{self.BASE_URL}/ticker/price")
            response.raise_for_status()
            all_prices = response.json()
            
            usdc_prices = {
                item['symbol']: item['price']
                for item in all_prices
                if item['symbol'].endswith('USDC')
            }
            return usdc_prices
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all prices: {e}")
            return {}


def format_price_output(symbol: str, data: Dict) -> str:
    """Format price data for display"""
    if not data:
        return f"{symbol}: Error fetching data"
    
    if 'priceChange' in data:  # 24h ticker data
        return (
            f"\n{symbol}:\n"
            f"  Current Price: {float(data['lastPrice']):,.8f} USDC\n"
            f"  24h Change: {float(data['priceChange']):,.8f} ({data['priceChangePercent']}%)\n"
            f"  24h High: {float(data['highPrice']):,.8f} USDC\n"
            f"  24h Low: {float(data['lowPrice']):,.8f} USDC\n"
            f"  24h Volume: {float(data['volume']):,.2f}"
        )
    else:  # Simple price data
        return f"{symbol}: {float(data['price']):,.8f} USDC"


def main():
    """Main function with CLI interface"""
    fetcher = BinanceUSDCPriceFetcher()
    
    if len(sys.argv) == 1:
        print("Binance USDC Price Fetcher")
        print("=" * 50)
        print("\nUsage:")
        print("  python binance_usdc_prices.py list              - List all USDC pairs")
        print("  python binance_usdc_prices.py all               - Get all USDC pair prices")
        print("  python binance_usdc_prices.py <SYMBOL>          - Get price for specific pair")
        print("  python binance_usdc_prices.py <SYMBOL> --full   - Get detailed 24h stats")
        print("\nExamples:")
        print("  python binance_usdc_prices.py BTCUSDC")
        print("  python binance_usdc_prices.py ETHUSDC --full")
        return
    
    command = sys.argv[1].upper()
    
    if command == "LIST":
        print("Available USDC Trading Pairs:")
        print("=" * 50)
        pairs = fetcher.get_all_usdc_pairs()
        for i, pair in enumerate(pairs, 1):
            print(f"{i:3d}. {pair}")
        print(f"\nTotal: {len(pairs)} pairs")
        
    elif command == "ALL":
        print("Fetching all USDC pair prices...")
        print("=" * 50)
        prices = fetcher.get_all_usdc_prices()
        for symbol, price in sorted(prices.items()):
            print(f"{symbol:15s}: {float(price):>15,.8f} USDC")
        print(f"\nTotal: {len(prices)} pairs")
        
    else:
        symbol = command
        if not symbol.endswith('USDC'):
            symbol += 'USDC'
        
        full_stats = '--full' in [arg.lower() for arg in sys.argv]
        
        if full_stats:
            print(f"Fetching detailed statistics for {symbol}...")
            print("=" * 50)
            data = fetcher.get_ticker_24h(symbol)
            print(format_price_output(symbol, data))
        else:
            print(f"Fetching price for {symbol}...")
            print("=" * 50)
            data = fetcher.get_price(symbol)
            print(format_price_output(symbol, data))


if __name__ == "__main__":
    main()
