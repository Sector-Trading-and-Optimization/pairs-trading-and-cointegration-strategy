# Pairs Trading and Cointegration Strategy

A Python implementation of statistical arbitrage using pairs trading based on cointegration analysis. This project demonstrates how to identify cointegrated stock pairs, generate trading signals using z-score analysis, and backtest the strategy performance.

## Developer 

Pratyush Kumar Swain : [Github](https://github.com/Pratyush439), [LinkedIn](https://www.linkedin.com/in/pratyush-kumar-swain-2313482a5/)
Arsh Chand : [Github](https://github.com/ArshChand), [LinkedIn](www.linkedin.com/in/arsh-chand)
Kavya Kumar Agrawal : [Github](https://github.com/Kavya-Agrawal), [LinkedIn](https://www.linkedin.com/in/kavya-kumar-agrawal/)
Sanidhya Srivastava : [Github](https://github.com/ArshChand), [LinkedIn](www.linkedin.com/in/arsh-chand)
Bhavya Bharti : [Github](https://github.com/ArshChand), [LinkedIn](www.linkedin.com/in/arsh-chand)

## Overview

This pairs trading strategy identifies two stocks that historically move together (cointegrated) and trades on temporary divergences from their long-term equilibrium relationship. The implementation uses statistical tests to find cointegrated pairs and generates buy/sell signals when the spread between assets deviates significantly from its mean.

## Key Features

- **Multi-Stock Analysis**: Analyzes 20 major stocks including AAPL, MSFT, GOOGL, AMZN, TSLA, JPM, and others
- **Cointegration Testing**: Automated detection of cointegrated pairs using statistical tests
- **Correlation Analysis**: Comprehensive correlation matrix visualization
- **Signal Generation**: Z-score based trading signals with configurable thresholds
- **Portfolio Simulation**: Complete backtesting with P&L calculation
- **Visualization**: Interactive plots for price movements, spreads, z-scores, and trading signals

## Strategy Logic

### 1. Data Collection
- Downloads historical stock data from Yahoo Finance (2017-2023)
- Focuses on 20 large-cap stocks across different sectors
- Splits data into training and testing sets

### 2. Pair Selection
- Calculates correlation matrix for all stock pairs
- Performs cointegration tests to identify statistically significant pairs
- Filters pairs with p-value < 0.05 for cointegration

### 3. Spread Construction
- Uses logarithmic regression to determine optimal hedge ratio
- Constructs spread as: `Spread = log(Stock2) - β × log(Stock1)`
- Monitors spread for mean-reverting behavior

### 4. Signal Generation
- Calculates z-score of the spread: `z = (spread - mean) / std`
- **Buy Signal**: When z-score < -1 (spread is undervalued)
- **Sell Signal**: When z-score > 1 (spread is overvalued)
- **Exit**: When z-score returns to neutral territory

### 5. Portfolio Management
- Equal capital allocation ($50,000) to each stock
- Long/short positions based on spread signals
- Continuous P&L tracking and performance evaluation

## Installation

```bash
# Install required packages
pip install yfinance pandas numpy matplotlib seaborn statsmodels scikit-learn
```

## Dependencies

```python
yfinance          # Stock data retrieval
pandas           # Data manipulation
numpy            # Numerical computations
matplotlib       # Basic plotting
seaborn          # Statistical visualizations
statsmodels      # Statistical tests and regression
scikit-learn     # Data splitting utilities
```

## Usage

### 1. Run the Complete Analysis

```python
# The main script includes all steps:
python pipeline.py
```

### 2. Key Functions

#### Find Cointegrated Pairs
```python
def find_cointegrated_pairs(data):
    """
    Identifies cointegrated pairs from price data
    Returns p-value matrix and list of significant pairs
    """
    n = data.shape[1]
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            result = coint(data[keys[i]], data[keys[j]])
            pvalue_matrix[i, j] = result[1]
            if result[1] < 0.05:
                pairs.append((keys[i], keys[j]))
    return pvalue_matrix, pairs
```

#### Generate Trading Signals
```python
def generate_trade_signals(S1, S2, spread, zscore):
    """
    Creates buy/sell signals based on z-score thresholds
    Returns DataFrame with positions and signals
    """
    trades = pd.DataFrame({
        'price1': S1, 'price2': S2, 'spread': spread, 'zscore': zscore
    })
    trades['signal1'] = np.where(trades['zscore'] > 1, -1, 
                        np.where(trades['zscore'] < -1, 1, 0))
    trades['signal2'] = -trades['signal1']
    return trades
```

#### Calculate P&L
```python
def pnl_calculation(signals):
    """
    Simulates portfolio performance with $50,000 initial capital per stock
    Returns portfolio DataFrame with holdings, cash, and total values
    """
    initial_capital = 50000
    # Implementation details in main code
    return portfolio
```

## Example Output

### Identified Cointegrated Pairs
The algorithm automatically identifies cointegrated pairs from the stock universe. Example pairs might include:
- ('JNJ', 'V') - Featured pair in the analysis
- ('AAPL', 'MSFT') - Technology sector pairs
- ('KO', 'PG') - Consumer goods pairs

### Trading Signals Visualization
- **Green triangles (▲)**: Buy signals when z-score < -1
- **Red triangles (▼)**: Sell signals when z-score > 1
- **Blue line**: Z-score evolution over time

### Performance Metrics
The strategy tracks:
- Total portfolio value over time
- Individual stock performance
- Cash positions and holdings
- Return calculations

## Project Structure

```
pairs-trading-strategy/
├── Data/
    ├── JNJ.csv  
    └── V.csv 
├── Notebooks/
    └── pairs_trading.ipynb. #Notebook File with Results
├── Src/
    ├── pipeline.py
    ├── strategy.py   
    └── utils.py 
└── Results/
    ├── correlation_matrix.png  # Asset correlation heatmap
    ├── closing_data.png    # closing prices 
    ├── residual_spread.png     # Residuals plot
    ├── zscore.png        # Z-score with thresholds
    ├── rel_close_data.png     # Relative price movements
    ├── signals.png   # Buy/sell signal visualization
    └── equity_curve.png # P&L chart
```

## Key Parameters

```python
# Stock Universe
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "WMT", 
          "JNJ", "V", "PG", "KO", "NFLX", "DIS", "NVDA", "VZ", 
          "T", "IBM", "HD", "BA", "MA"]

# Time Period
start_date = '2017-06-01'
end_date = '2023-07-31'

# Trading Thresholds
entry_threshold = 1.0    # Z-score for entry signals
exit_threshold = 0.0     # Z-score for exit signals

# Portfolio Settings
initial_capital = 50000  # Per stock allocation
test_size = 0.5         # Train/test split ratio
```

## Strategy Performance

### Featured Pair: JNJ vs V
- **Cointegration**: Statistically significant relationship
- **Trading Logic**: Long JNJ / Short V when spread is low, reverse when high
- **Visualization**: Complete analysis with price charts, spread analysis, and signal generation

### Risk Considerations
- **Market Risk**: Strategy performance depends on continued cointegration
- **Execution Risk**: Real-world transaction costs and slippage not included
- **Model Risk**: Historical relationships may not persist in future

## Customization

### Modify Stock Universe
```python
# Add or remove stocks from the analysis
stocks = ["YOUR", "CUSTOM", "STOCK", "LIST"]
```

### Adjust Trading Thresholds
```python
# More conservative approach
entry_threshold = 2.0
exit_threshold = 0.5

# More aggressive approach  
entry_threshold = 0.5
exit_threshold = 0.0
```

### Change Time Period
```python
start = '2020-01-01'
end = '2024-01-01'
```

## Results Interpretation

1. **Correlation Matrix**: Shows linear relationships between all stock pairs
2. **Cointegration Results**: Lists statistically significant cointegrated pairs
3. **Spread Analysis**: Visualizes the mean-reverting behavior of selected pairs
4. **Trading Signals**: Shows entry/exit points based on z-score thresholds
5. **Portfolio Performance**: Tracks cumulative P&L over the backtesting period

## Disclaimer

This code is for educational and research purposes only. Past performance does not guarantee future results. Trading involves substantial risk of loss and is not suitable for all investors. Always conduct thorough testing and consider consulting with financial professionals before implementing any trading strategy.

## References

- Engle-Granger Cointegration Test
- Johansen Cointegration Test  
- Statistical Arbitrage Literature
- Pairs Trading Academic Papers

## Contributing

Feel free to fork this repository and submit pull requests for improvements. Suggested areas for contribution:
- Enhanced visualization features
- Additional statistical tests
- Performance optimization
- Extended backtesting metrics

---

**Note**: This implementation uses actual market data and demonstrates real statistical relationships between stocks, making it a practical foundation for pairs trading research and development.
