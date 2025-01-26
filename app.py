from flask import Flask, render_template, request, redirect, url_for, flash
import os
from utils import load_watchlist, save_watchlist, fetch_stock_data

TEMPLATE_DIR = os.path.abspath("template")
STATIC_DIR = os.path.abspath("static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'ABCDEFG'

@app.route('/start-flask')
def start_flask():
    try:
        subprocess.Popen(["python", "app.py"])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/', methods=['GET', 'POST'])
def index():
    tickers = load_watchlist()  # ✅ Always reload from file
    print("📌 Watchlist before adding:", tickers)  # Debugging

    if request.method == 'POST':
        ticker = request.form.get('ticker').upper().strip()
        if not ticker:
            flash('Please enter a ticker symbol', 'error')
        else:
            data = fetch_stock_data(ticker)
            if data:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)  # ✅ Now correctly saving new ticker
                    flash(f'{ticker} added to watchlist.', 'success')
                else:
                    flash(f'{ticker} is already in your watchlist.', 'info')
            else:
                flash(f'Problem fetching data for {ticker}', 'error')

    stocks_data = [fetch_stock_data(ticker) for ticker in tickers if fetch_stock_data(ticker)]
    print("✅ Watchlist after adding:", tickers)  # Debugging
    return render_template('stockwatch.html', stocks=stocks_data)

@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlist()
    print("Before removal:", tickers)  # Debugging line
    if ticker in tickers:
        tickers.remove(ticker)
        print("After removal:", tickers)  # Debugging line
        save_watchlist(tickers)  # ✅ Now it correctly updates the file
        flash(f'{ticker} removed.', 'success')
    else:
        flash(f'{ticker} not in list.', 'error')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
