from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL"]
        self.lookback_period = 5  # SMA lookback period

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Choosing '1day' for daily moving average computations
        return "1day"

    def run(self, data):
        sma_diffs = {}
        # Calculate the difference between the last close and the SMA for each asset
        for ticker in self.tickers:
            sma = SMA(ticker, data["ohlcv"], self.lookback_period)
            if sma and len(sma) > 0:
                current_price = data["ohlcv"][-1][ticker]["close"]
                sma_diffs[ticker] = current_price - sma[-1]
        
        # Determine the most underperforming stock based on SMA difference
        if not sma_diffs:
            return TargetAllocation({})
        
        underperforming_stock = min(sma_diffs, key=sma_diffs.get)
        
        # Allocate more to the underperforming stock
        allocation = {ticker: 0 for ticker in self.tickers}
        allocation[underperforming_stock] = 1  # Full allocation to the underperforming stock

        log(f"Allocating to underperforming stock: {underperforming_stock}")
        return TargetAllocation(allocation)