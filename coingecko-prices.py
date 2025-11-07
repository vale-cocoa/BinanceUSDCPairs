#!/usr/bin/env python3
"""
Alternative: Fetch USDC prices from CoinGecko API
More reliable for GitHub Actions as CoinGecko is more permissive with datacenter IPs
"""

import requests
import json
from datetime import datetime

def fetch_coingecko_prices():
    """Fetch crypto prices from CoinGecko (no auth needed)"""
    
    # Major coins we want to track
    coins = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'binancecoin': 'BNB',
        'solana': 'SOL',
        'cardano': 'ADA',
        'dogecoin': 'DOGE',
        'ripple': 'XRP',
        'polkadot': 'DOT',
        'avalanche-2': 'AVAX',
        'chainlink': 'LINK'
    }
    
    try:
        # CoinGecko free API - no key needed
        coin_ids = ','.join(coins.keys())
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_ids,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Format output
        output = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'source': 'CoinGecko API',
            'prices': {}
        }
        
        for coin_id, symbol in coins.items():
            if coin_id in data:
                coin_data = data[coin_id]
                output['prices'][f'{symbol}/USDC'] = {
                    'price': coin_data.get('usd', 0),
                    'change_24h': coin_data.get('usd_24h_change', 0),
                    'volume_24h': coin_data.get('usd_24h_vol', 0)
                }
        
        return output
        
    except Exception as e:
        print(f"Error fetching from CoinGecko: {e}")
        return None

def main():
    print("Fetching prices from CoinGecko...")
    data = fetch_coingecko_prices()
    
    if data:
        # Save to JSON
        with open('prices_data_coingecko.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        # Create markdown summary
        with open('PRICE_SUMMARY_COINGECKO.md', 'w') as f:
            f.write(f"# Crypto Prices (CoinGecko)\n\n")
            f.write(f"**Last Updated:** {data['timestamp']}\n\n")
            f.write(f"**Source:** {data['source']}\n\n")
            
            for pair, info in sorted(data['prices'].items()):
                symbol = pair.split('/')[0]
                price = info['price']
                change = info['change_24h']
                volume = info['volume_24h']
                
                emoji = "🟢" if change >= 0 else "🔴"
                f.write(f"### {emoji} {pair}\n\n")
                f.write(f"- **Price:** ${price:,.2f}\n")
                f.write(f"- **24h Change:** {change:+.2f}%\n")
                f.write(f"- **24h Volume:** ${volume:,.0f}\n\n")
        
        print(f"✓ Successfully fetched {len(data['prices'])} prices")
        print("✓ Saved to prices_data_coingecko.json")
        print("✓ Saved summary to PRICE_SUMMARY_COINGECKO.md")
        
    else:
        print("✗ Failed to fetch prices")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
