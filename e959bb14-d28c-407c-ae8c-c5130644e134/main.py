from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers for firearm companies
        self.tickers = ["RGR", "SWBI", "AOBC"]  # Examples: 'RGR' for Sturm, Ruger & Co., 'SWBI' Smith & Wesson
        # Adding SocialSentiment data to monitor sentiment changes, can be a proxy to gauge public interest or concern
        self.data_list = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        # Daily analysis, could be adjusted per strategy needs
        return "1day"

    @property
    def assets(self):
        # The stocks we are interested to trade
        return self.tickers

    @property
    def data(self):
        # The data required to run this strategy
        return self.data_list

    def run(self, data):
        # Initializing our target allocation with equal distribution assuming no prior knowledge
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        
        # Example strategy implementation
        # For a more sophisticated approach, you could incorporate sentiment analysis, news analysis, etc.
        # This example equally distributes investment among selected tickers

        # As this strategy is based on an external event (election outcome), the run method here doesn't dynamically adjust allocations
        # A more advanced strategy might analyze real-time data, such as sentiment or market reactions, to adjust allocations dynamically
        
        return TargetAllocation(allocation_dict)