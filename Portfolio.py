from pandas_datareader import data as pdr

class Portfolio:
    def __init__(self, stocks, weights, value, start, end):
        self.stocks = stocks
        self.weights = weights
        self.start = start
        self.end = end
        self.value = value

    def load_data(self):
        self.stock_data = {}
        for stock in self.stocks:
            data = pdr.get_data_yahoo(stock, self.start, self.end)
            data = data.drop(['Adj Close'], axis=1)
            data.reset_index(inplace=True)
            self.stock_data[stock] = data

        portfolio_data = pdr.get_data_yahoo(self.stocks, self.start, self.end)
        portfolio_data = portfolio_data['Close']
        returns = portfolio_data.pct_change()
        self.mean_returns = returns.mean() # mean return of stock from time period
        self.cov_matrix = returns.cov() # covariance matrix between stock returns

    def get_weights(self):
        return self.weights
    
    def get_data(self):
        return self.stock_data
    
    def get_mean_returns(self):
        return self.mean_returns
    
    def get_cov_matrix(self):
        return self.cov_matrix
    
    def get_num_stocks(self):
        return len(self.stocks)
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value