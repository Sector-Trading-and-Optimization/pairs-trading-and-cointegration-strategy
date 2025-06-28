import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import coint

def fetch_close_prices(tickers, start, end):
    df = pd.DataFrame()
    for t in tickers:
        data = yf.Ticker(t).history(start=start, end=end)
        df[t] = data['Close']
    return df

def split_data(companies, test_size=0.5):
    return train_test_split(companies, test_size=test_size, shuffle=False)

def compute_correlation(df):
    return df.pct_change().corr()

def find_cointegrated_pairs(df, alpha=0.05):
    n = df.shape[1]
    keys = df.columns
    pvals = np.ones((n,n))
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            p = coint(df[keys[i]], df[keys[j]])[1]
            pvals[i,j] = p
            if p < alpha:
                pairs.append((keys[i], keys[j]))
    return pvals, pairs