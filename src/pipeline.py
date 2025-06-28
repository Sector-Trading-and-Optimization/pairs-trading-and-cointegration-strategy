import datetime
import yfinance as yf
from utils import fetch_close_prices, split_data, compute_correlation, find_cointegrated_pairs
from strategy import (fit_spread, compute_zscore, generate_trade_signals,
                      show_trade_signals, pnl_calculation, plot_portfolio_value)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Setup
    stocks = ["AAPL","MSFT","GOOGL","AMZN","TSLA","JPM","WMT",
              "JNJ","V","PG","KO","NFLX","DIS","NVDA","VZ","T",
              "IBM","HD","BA","MA"]
    start, end = '2017-06-01', '2023-07-31'

    # Fetch data
    companies = fetch_close_prices(stocks, start, end)
    print(companies.head())

    # Train/test split
    train_close, test_close = split_data(companies)

    # Correlation heatmap
    fig, ax = plt.subplots(figsize=(20,14))
    sns.heatmap(train_close.pct_change().corr(), ax=ax, cmap='coolwarm', annot=True, fmt='.3f')
    ax.set_title('Assets Correlation Matrix')
    plt.show()

    # Cointegration
    pvalues, pairs = find_cointegrated_pairs(train_close)
    print('Pairs:', pairs)

    # Choose pair
    asset1, asset2 = 'JNJ','V'
    train = pd.DataFrame({'asset1': train_close[asset1], 'asset2': train_close[asset2]})
    ax = train.plot(figsize=(12,6), title=f'Daily Closing Prices for {asset1} and {asset2}')
    ax.set_ylabel('Closing Price'); ax.grid(True)
    plt.show()

    # Relative price plot
    plt.figure(figsize=(14,6))
    rel1 = companies[asset1]/companies[asset1].iloc[0]
    rel2 = companies[asset2]/companies[asset2].iloc[0]
    plt.plot(rel1, label=asset1); plt.plot(rel2, label=asset2)
    plt.xlabel('Time'); plt.ylabel('Rel Close Price'); plt.legend(); plt.show()

    # OLS spread & z-score
    beta, spread = fit_spread(companies[asset2], companies[asset1])
    errors = spread
    plt.figure(figsize=(14,6))
    errors.plot(label=f'x = {asset1}; y = {asset2}'); plt.title(f'Residuals from spread Spread = {asset2} + {beta:.2f}*{asset1}'); plt.show()
    zscore = compute_zscore(spread)
    plt.figure(figsize=(14,6))
    zscore.plot(label='z-score'); plt.axhline(1, color='b'); plt.axhline(-1, color='b'); plt.title(f'z-score {asset2}-{asset1}'); plt.show()

    # Signals & PnL
    trade_signals = generate_trade_signals(companies[asset2], companies[asset1], spread, zscore)
    show_trade_signals(trade_signals, asset1, asset2)
    portfolio = pnl_calculation(trade_signals)
    print(portfolio.head())
    plot_portfolio_value(portfolio)

if __name__ == '__main__':
    main()
