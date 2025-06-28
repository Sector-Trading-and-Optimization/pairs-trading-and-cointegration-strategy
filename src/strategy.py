import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

def fit_spread(y, x):
    ly = np.log(y)
    lx = np.log(x)
    Xc = sm.add_constant(lx)
    model = sm.OLS(ly, Xc).fit()
    beta = model.params[1]
    spread = ly - beta * lx
    return beta, spread

def compute_zscore(spread):
    return (spread - spread.mean()) / spread.std()

def generate_trade_signals(S1, S2, spread, zscore, entry=1):
    trades = pd.DataFrame({
        'price1': S1,
        'price2': S2,
        'spread': spread,
        'zscore': zscore
    }).dropna()
    trades['signal1'] = np.where(trades.zscore > entry, -1,
                          np.where(trades.zscore < -entry, 1, 0))
    trades['signal2'] = -trades.signal1
    trades['position1'] = trades.signal1.diff().apply(lambda x: 0 if abs(x)>1 else x)
    trades['position2'] = trades.signal2.diff().apply(lambda x: 0 if abs(x)>1 else x)
    return trades

def show_trade_signals(data, name1, name2):
    fig, ax = plt.subplots(figsize=(14,6))
    ax.plot(data.zscore, color='#4abdac')
    ax.plot(data.zscore[data.position1==1], lw=0, marker='^', c='g', markersize=8)
    ax.plot(data.zscore[data.position1==-1], lw=0, marker='v', c='r', markersize=8)
    ax.set_title(f'{name2} vs {name1}')
    ax.legend(['Z-Score','Buy','Sell'])
    plt.show()

def pnl_calculation(signals, initial=50000):
    shares1 = initial // signals.price1.iloc[0]
    shares2 = initial // signals.price2.iloc[0]
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['holdings1'] = signals.position1.cumsum() * signals.price1 * shares1
    portfolio['cash1'] = initial - (signals.position1 * signals.price1 * shares1).cumsum()
    portfolio['total1'] = portfolio.holdings1 + portfolio.cash1
    portfolio['return1'] = portfolio.total1.pct_change()
    portfolio['holdings2'] = signals.position2.cumsum() * signals.price2 * shares2
    portfolio['cash2'] = initial - (signals.position2 * signals.price2 * shares2).cumsum()
    portfolio['total2'] = portfolio.holdings2 + portfolio.cash2
    portfolio['return2'] = portfolio.total2.pct_change()
    portfolio['total'] = portfolio.total1 + portfolio.total2
    return portfolio.dropna()

def plot_portfolio_value(portfolio):
    fig, ax = plt.subplots(figsize=(14,6))
    ax.plot(portfolio.total, c='g')
    ax.set_ylabel('Asset Value', labelpad=15)
    ax.set_xlabel('Date', labelpad=15)
    ax.set_title('Portfolio Performance PnL')
    ax.legend(['Total Portfolio Value'])
    plt.show()