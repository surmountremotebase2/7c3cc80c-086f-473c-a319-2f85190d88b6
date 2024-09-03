from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers for the pairs you want to trade
        self.tickers = ["AAPL", "GOOGL"]

        # Here, we're only adding placeholder data for demonstration. 
        # In a real strategy, you'd include relevant data for both analysis and signals.
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers]
        self.data_list += [InsiderTrading(i) for i in self.tickers]

    @property
    def interval(self):
        # Define the data interval. This should match your trading signal requirements.
        return "1day"

    @property
    def assets(self):
        # List the assets that the strategy will trade.
        return self.tickers

    @property
    def data(self):
        # Return the data required for your strategy.
        return self.data_list

    def run(self, data):
        # This is where you would implement your trading logic.
        # Below is a placeholder logic for equally weighting both assets.
        # Real-world strategies would use market data and statistical analysis for decision making.

        allocation_dict = {ticker: 0.5 for ticker in self.tickers}  # Equal weighting

        # Example logic: This just checks if there are insider trades and logs it (does not affect allocation)
        for asset in self.data_list:
            if asset.__class__.__name__ == "InsiderTrading":
                trades = data[(asset.__class__.__name__.lower(), asset.symbol)]
                if trades:
                    log(f"Insider trades for {asset.symbol}: {len(trades)}")

        # Return the target allocation.
        # Note: This example doesn't genuinely analyze AAPL and GOOGL pair dynamics. 
        # For a practical strategy, consider historical correlation, pairs trading cointegration tests, etc.
        return TargetAllocation(allocation_dict)