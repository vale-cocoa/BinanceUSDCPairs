# GitHub Binance Price Fetcher Setup

This setup will automatically fetch Binance USDC prices every 15 minutes and commit them to your GitHub repository, making them accessible to Claude during trading discussions.

## Setup Instructions

### 1. Create a New GitHub Repository

1. Go to https://github.com/new
2. Name it something like `binance-price-tracker`
3. Make it **Public** (so Claude can access it without authentication)
4. Initialize with a README (optional)

### 2. Upload Files to Your Repository

Upload these files to your repository:
- `binance_usdc_prices.py` - The price fetching script
- `.github/workflows/fetch-binance-prices.yml` - The GitHub Action workflow
- `requirements.txt` - Python dependencies

You can do this via:
- **Web UI:** Click "Add file" → "Upload files"
- **Git CLI:**
  ```bash
  git clone https://github.com/YOUR_USERNAME/binance-price-tracker.git
  cd binance-price-tracker
  # Copy the files here
  git add .
  git commit -m "Add Binance price fetcher"
  git push
  ```

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"

### 4. Verify It's Working

The workflow will run:
- **Every 15 minutes** automatically
- **Manually** - Go to Actions → "Fetch Binance USDC Prices" → "Run workflow"
- **On push** - When you update the Python script

After the first run, you should see these files in your repo:
- `prices_output.txt` - Raw output from the script
- `prices_data.json` - Structured JSON data
- `PRICE_SUMMARY.md` - Human-readable markdown summary

### 5. Share the Repository URL with Claude

Once set up, share your repository URL with Claude. For example:
```
https://github.com/YOUR_USERNAME/binance-price-tracker
```

Claude can then fetch the latest prices during your trading conversations using:
```
https://raw.githubusercontent.com/YOUR_USERNAME/binance-price-tracker/main/prices_data.json
```

## Files Generated

### `prices_data.json`
Structured data with all prices and detailed stats:
```json
{
  "timestamp": "2024-11-07T12:30:00Z",
  "all_prices": {
    "BTCUSDC": "43250.50000000",
    "ETHUSDC": "2285.75000000",
    ...
  },
  "major_pairs_24h_stats": {
    "BTCUSDC": {
      "lastPrice": "43250.50",
      "priceChangePercent": "2.98",
      "highPrice": "43500.00",
      ...
    }
  }
}
```

### `PRICE_SUMMARY.md`
Human-readable summary with emojis and formatting - great for quick reference!

### `prices_output.txt`
Raw text output from the command line tool.

## Customization

### Change Update Frequency
Edit `.github/workflows/fetch-binance-prices.yml`:
```yaml
schedule:
  - cron: '*/15 * * * *'  # Every 15 minutes
  # Examples:
  # - cron: '*/5 * * * *'   # Every 5 minutes
  # - cron: '0 * * * *'     # Every hour
  # - cron: '0 */4 * * *'   # Every 4 hours
```

### Track Different Pairs
Edit the `major_pairs` list in the workflow:
```python
major_pairs = ['BTCUSDC', 'ETHUSDC', 'BNBUSDC', 'SOLUSDC', 'ADAUSDC', 'DOGEUSDC']
```

### Add More Detailed Stats
You can modify the workflow to fetch additional pairs or different timeframes.

## Troubleshooting

### Workflow Not Running
- Check that Actions are enabled in your repository settings
- Verify the workflow file is in `.github/workflows/` directory
- Check the Actions tab for any error messages

### Python Errors
- Make sure `binance_usdc_prices.py` is in the root of your repository
- Check the Actions logs for specific error messages

### Rate Limits
- Binance API has rate limits (1200 requests/minute)
- The default 15-minute interval is very safe
- Don't set it too frequently (avoid every 1-2 minutes)

## Privacy & Security

- This uses Binance's **public API** (no API keys needed)
- The repository should be **public** so Claude can access it
- No sensitive information is stored
- Only reads market data (cannot make trades)

## Usage with Claude

Once set up, you can say things like:

> "Claude, check the latest Bitcoin price from my GitHub repo at https://github.com/USERNAME/binance-price-tracker"

> "What's the 24h change for ETH? Check my price tracker."

> "Analyze the current USDC pairs - fetch from my repo"

Claude will automatically fetch the latest data and can help you analyze trading opportunities!

## Cost

- **GitHub Actions:** Free for public repositories (2,000 minutes/month)
- **Binance API:** Free (public endpoints)
- **Total Cost:** $0 🎉

## Next Steps

After setup, you can:
1. Set up price alerts based on the data
2. Create visualizations or charts
3. Build a trading dashboard
4. Integrate with other tools
5. Add more exchanges or trading pairs

Happy trading! 📈
