import numpy as np

class MonteCarloSim:
    def __init__(self, num_sims, time_frame, portfolio):
        self.num_sims = num_sims
        self.time_frame = time_frame
        self.num_stocks = portfolio.get_num_stocks()
        self.weights = portfolio.get_weights()
        self.mean_returns = portfolio.get_mean_returns()
        self.cov_matrix = portfolio.get_cov_matrix()
        self.portfolio_value = portfolio.get_value()
        self.simulation_data = None

    def run_sumulations(self):
        self.simulation_data = np.full(shape=(self.time_frame + 1, self.num_sims), fill_value=0.0)
        meanMatrix = np.full(shape=(self.time_frame, self.num_stocks), fill_value=self.mean_returns)
        meanMatrix = meanMatrix.T
        L = np.linalg.cholesky(self.cov_matrix) # cholesky decomposition

        for m in range(self.num_sims):
            Z = np.random.normal(size=(self.time_frame, self.num_stocks))
            dailyReturns = meanMatrix + np.inner(L, Z)
            self.simulation_data[:, m] = np.concatenate([np.array([self.portfolio_value]) ,np.cumprod(np.inner(self.weights, dailyReturns.T) + 1) * self.portfolio_value])
        
        return self.simulation_data

    def  get_mc_average(self):
        return np.round(self.simulation_data[-1:].mean(axis=1))
    
    def get_final_values(self):
        return np.round(self.simulation_data[-1:])
    

