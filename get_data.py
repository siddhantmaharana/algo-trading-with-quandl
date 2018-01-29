import quandl
import pandas as pd
import numpy as numpy



##initialize quandl endpoints
API_KEY = 'XLfayzPbPyUTxm51FGVj'
QUANDL_ENDPOINT = 'https://www.quandl.com/api/v3/datasets.json'
quandl.ApiConfig.api_key = API_KEY


def main():
	## fetching stocks symbols to get the data 

	start_date = '2016-01-01'
	end_date = '2018-01-01'
	stock_data = open('nifty_50.txt')

	#getting data for individual stocks
	for line in stock_data:
		stock_symbol = line.rstrip()
		fetch_data_from_quandl(stock_symbol,start_date,end_date)




def fetch_data_from_quandl(symbol, start_date, end_date):

	stock_code = 'NSE/' + symbol
	df_list =[]
	try:
		print ('getting data for %s' %(symbol))
		stock_data = quandl.Dataset(stock_code).data(params={'start_date': start_date, 'end_date': end_date}).to_pandas()
		stock_data = stock_data.drop('Turnover (Lacs)', 1)
		stock_data = stock_data.drop('Last', 1)
		stock_data = stock_data.rename_axis({"Total Trade Quantity": "Volume"}, axis="columns")
		stock_data['Symbol'] = symbol
		stock_data.to_csv('data/%s.csv'%(symbol))
		return stock_data

	except:
		print ('Skipping %s'%(symbol))


    	
if __name__ == '__main__':
	main()