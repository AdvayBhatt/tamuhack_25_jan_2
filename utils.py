import json
import yfinance as yf

WATCHLIST = 'watchlist.json'

#def save_watchlist(tickers):
#    with open(WATCHLIST, 'w') as f:
#        json.dump(tickers, f)

def save_watchlist(tickers):
    """ Save the updated watchlist to watchlist.txt """
    try:
        with open("watchlist.txt", "w") as f:
            for ticker in tickers:
                f.write(ticker + "\n")
        print("✅ Watchlist updated:", tickers)  # Debugging
    except Exception as e:
        print("❌ Error saving watchlist:", e)  # Debugging

def load_watchlist():
    """ Load the watchlist from watchlist.txt """
    try:
        with open("watchlist.txt", "r") as f:
            tickers = [line.strip() for line in f.readlines()]
        print("✅ Loaded watchlist from file:", tickers)  # Debugging
        return tickers
    except FileNotFoundError:
        print("⚠️ Watchlist file not found, returning empty list")
        return []

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            row = data.iloc[-1]
            price = row['Close']
            high = row['High']
            low = row['Low']
            volume = row['Volume']
            prev_close = stock.info.get('previousClose', price)
            change = price - prev_close
            change_pct = (change/prev_close)*100 if prev_close else 0
            date_time = row.name.strftime("%Y-%m-%d %H:%M:%S")

            return_data = {
                'ticker': ticker,
                'price': f'${price:.2f}',
                'date_time': date_time,
                'change': change,
                'change_pct': change_pct,
                'high': f'${high:.2f}',
                'low': f'${low:.2f}',
                'volume': f'${volume:,}'
            }

            return return_data
        else:
            return None
    except Exception:
        return None


