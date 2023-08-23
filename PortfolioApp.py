import streamlit as st
import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import plotly.express as px
from pandas_datareader import data as pdr
from MonteCarloSim import MonteCarloSim
from Portfolio import Portfolio

yf.pdr_override()

START = (dt.datetime.now() - dt.timedelta(weeks=1560)).strftime('%Y-%m-%d')
END = dt.datetime.now().strftime('%Y-%m-%d')
PORTFOLIO_TO_STOCKS = {
    'TWO-FUND' : ['VTI', 'VBTLX'],
    'THREE-FUND' : ['VTI', 'VXUS', 'VBTLX'],
}
TICKER_TO_NAME = {
    'VTI' : 'Vanguard Total Stock Market Index Fund ETF',
    'VBTLX' : 'Vanguard Total Bond Market Index Fund Admiral Shares',
    'VXUS' : 'Vanguard Total International Stock Index Fund ETF',
 }
PORTFOLIO_DESCRIPTION = {

    'TWO-FUND' : '''The two fund portfolio represents an asset management strategy where one\'s assets allocations are 
         divided between two fund (usually a total stock market 
         fund and a bond fun). For this example, 60 percent of the user's assets are 
         allocated to VTI, an ETF tracking the movement of the US Total Stock Market. The remaining
         40 percent are allocated to VBTLX, a total bond index. This management strategy adds additional levels of
          security relative to the one-fund approach, since bonds are not as volatile as stocks. ''',
    'THREE-FUND' : '''The three fund portfolio represents an asset management strategy where
         one\'s assets are allocated to a combination of three funds. For this example, an even split 
         between VTI, VXUS, and VBTLX is used. VTI and VXUS represent the US and Internatial total stock 
         markets, and VBTLX represents the US bond market. Out of the three portfolios shown, the three-fund approach
         is the most conservative since one's assets are diversified accross three differnt markets.''',
}
PORTFOLIO_WEIGHTS = {
    'ONE-FUND' : np.array([1]),
    'TWO-FUND' : np.array([.6, .4]),
    'THREE-FUND' : np.array([.333, .333, .333])
}
STOCK_TO_COLOR = {
    'VTI' : '#eed9a4',
    'VBTLX' : '#f77876',
    'VXUS' : '#f6a978'
}
SIMS = 30 # number of simulations


st.title('Portfolio Monte Carlo Simulation')

portfolios = ('TWO-FUND', 'THREE-FUND')
selected_portfolio = st.selectbox('Select Portfolio For Prediction', portfolios)
portfolio_stocks = PORTFOLIO_TO_STOCKS[selected_portfolio]
st.write(PORTFOLIO_DESCRIPTION[selected_portfolio])

portfolio = Portfolio(portfolio_stocks, PORTFOLIO_WEIGHTS[selected_portfolio], 0, START, END)
portfolio.load_data()

fig_pie = px.pie(values=portfolio.get_weights().tolist(), names=portfolio_stocks, color_discrete_sequence=px.colors.sequential.Agsunset_r)
st.plotly_chart(fig_pie)

value = 0
try:
    value = abs(int(st.text_input('Initial Portfolio Value')))
    portfolio.set_value(value)
except:
    st.write('Please enter a positive number')

n_years = st.slider('Years of Prediction', 1, 50)
period = n_years * 365

stock_data = portfolio.get_data()
mean_returns = portfolio.get_mean_returns()
cov_matrix = portfolio.get_cov_matrix()

st.subheader('Raw Data')
for stock in portfolio_stocks:
    st.write(TICKER_TO_NAME[stock] + f' ({stock})')
    st.write(stock_data[stock].tail())

def plot_raw_data():
    fig = go.Figure()
    fig.layout.update(title_text="Historical Time Series Data", xaxis_title='Year - slide to adjust', yaxis_title='Closing Price ($)', xaxis_rangeslider_visible=True, showlegend=True)
    for stock in portfolio_stocks:
        fig.add_trace(go.Scatter(x=stock_data[stock]['Date'], y=stock_data[stock]['Close'], name=stock, marker= {'color' : STOCK_TO_COLOR[stock]}))
    
    st.plotly_chart(fig)

plot_raw_data()

st.subheader('Monte Carlo Simulations')
st.write('Raw Data')

def monte_carlo_sim():
    mc = MonteCarloSim(SIMS, n_years * 265, portfolio)
    portfolio_sims = mc.run_sumulations()
    
    fig = go.Figure()
    fig.layout.update(title_text="Monte Carlo Graph", xaxis_title='Day - slide to adjust', yaxis_title='Portfolio Value ($)', xaxis_rangeslider_visible=True, showlegend=False)
    for m in range(SIMS):
        fig.add_trace(go.Scatter(x = np.arange(0, n_years * 365) , y = portfolio_sims[:, m]))

    portfolio_sims = pd.DataFrame(portfolio_sims, columns= ['Simulation ' + str(x) for x in range(1, SIMS + 1)])
    st.write(portfolio_sims)
    st.write('Final Value')
    st.write(mc.get_final_values())
    st.write(' Monte Carlo Average:')
    st.write(mc.get_mc_average())
    
    st.plotly_chart(fig)

monte_carlo_sim()
