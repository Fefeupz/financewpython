import pandas as pd
import yfinance as yf 

from bokeh.models.sources import ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import ColumnarDataSource, Select, DataTable, TableColumn
from bokeh.layouts import column, row
from bokeh.plotting import figure, show

default_tickers = ['AAPL', 'GOOG', 'MSFT', 'NFLX', 'TSLA']
START, END = '2018-01-01', '2021-01-01'

def load_ticker(tickers):
    df=yf.download(tickers, start=START, end=END)
    return df['Close'].dropna()

def get_data(t1, t2):
    d = load_ticker(default_tickers)
    df = d[[t1, t2]]
    returns = df.pct_change().add_suffix('_returns')
    df = pd.concat([df, returns], axis=1)
    df.rename(columns={t1:'t1', t2:'t2',
                       t1+'_returns':'t1_returns', t2+'_returns': 't2_returns'}, inplace=True)
    return df.dropna()

def nix(val, lst):
    return [x for x in lst if x!= val]

ticker1 = Select(value='AAPL', options = nix('GOOG', default_tickers))
ticker2 = Select(value="GOOG", options = nix('AAPL', default_tickers))

data = get_data(ticker1.value, ticker2.value)
source = ColumnDataSource (data=data)

corr_tools = 'pan, wheel_zoom, box_select, reset'
tools = 'pan, wheel_zoom, xbox_select, reset'

corr = figure(width=350, height=350, tools=corr_tools)
corr.circle('t1_returns', 't2_returns', size=2, source=source,
            selection_color = 'firbrick', alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)

show(corr)