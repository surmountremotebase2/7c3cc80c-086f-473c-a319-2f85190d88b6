from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, Ratios, FinancialStatement, InsiderTrading
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["GOOGL", "MSFT", "AAPL", "NVDA", "AMD"]  # Example AI-related stocks
        # Note: Replace these tickers with those of companies largely involved in AI if needed.
        self.data_list = [SocialSentiment(ticker) for ticker in self.tickers]
        self.data_list += [Ratios(ticker) for ticker in self.tickers]
        self.data_list += [FinancialStatement(ticker) for ticker in self.tickers]
        self.data_list += [InsiderTrading(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            sentiment_data = data.get(("social_sentiment", ticker), [])
            financial_data = data.get(("financial_statement", ticker), [])
            ratios_data = data.get(("ratios", ticker), [])
            insider_trading = data.get(("insider_trading", ticker), [])
            
            positive_sentiment = len([s for s in sentiment_data if s['twitterSentiment'] > 0.5 and s['stocktwitsSentiment'] > 0.5])
            strong_balance_sheet = any(f['totalCurrentAssets'] > f['totalCurrentLiabilities'] for f in financial_data)
            good_growth_potential = any(r['ebitdaGrowth'] > 0.10 for r in ratios_data)
            insider_confidence = not any(i['transactionType'] == "S-Sale" for i in insider_trading)
            
            # Combining sentiment with balance sheet and growth potential checks 
            # and insider buying as a signal for confidence in the company's prospects
            if positive_sentiment and strong_balance_sheet and good_growth_potential and insider_confidence:
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally weighted for simplicity; could be optimized
            else:
                allocation_dict[ticker] = 0  # No investment if conditions aren't met
        # Normalize allocations to ensure they sum up to 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 0:
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}
        else:  # Avoid division by zero if no conditions are met for any stock
            allocation_dict = {ticker: 0 for ticker in self.tickers}
        return TargetAllocation(allocation_dict)