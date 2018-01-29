import numpy as np
import pandas as pd


def get_results(stock_data):
	stock_data['st_dev'] = stock_data['Close'].rolling(window=90).std()
	stock_data['next_day_open'] = stock_data['Open'].shift(-1)
	stock_data['moving_average'] = stock_data['Close'].rolling(window=20).mean()
	stock_data['return_d0'] = (stock_data['Close'] - stock_data['Close'].shift(1))/ (stock_data['Close'].shift(1))
	stock_data['return_d1'] = (stock_data['Close'].shift(1) - stock_data['Close'].shift(2)) / (stock_data['Close'].shift(2))
	stock_data['return_d2'] = (stock_data['Close'].shift(2) - stock_data['Close'].shift(3)) / (stock_data['Close'].shift(3))
	# criteria 1 -- If the stock has grew for the last 3 days and the rate is in an increasing trend
	stock_data['criteria_1'] = np.where((stock_data['return_d0'] >= stock_data['return_d1']) & (stock_data['return_d1'] >= stock_data['return_d2']), 1,0)
	# if the return over last day is greater compared to the prev days
	stock_data['criteria_2'] = np.where((stock_data['return_d0'] - stock_data['return_d1']) >=  (stock_data['return_d1'] - stock_data['return_d2']),1,0)
	# if the gap down is less than the standard dev of the last 90 days
	stock_data['criteria_3'] = (stock_data['Open'] - stock_data['Low'].shift(1)) < stock_data['st_dev']
	# if the opening price is above the 20 day moving average
	stock_data['criteria_4'] = stock_data['Open'] > stock_data['moving_average']
	stock_data['buy'] = stock_data['criteria_1'] & stock_data['criteria_2'] & stock_data['criteria_3'] & stock_data['criteria_4']
	stock_data['g_l'] = ((stock_data['next_day_open'] - stock_data['Close']))/stock_data['Close']
	final_data = stock_data[stock_data.buy == 1]

	return final_data


