import pandas as pd
import numpy as np
from momentum import get_results
import os


def main():
	amount = 100000
	results_strategy =[]
	dir_path = os.path.abspath(os.path.dirname(__file__))
	stock_files_path = dir_path+'/data'

	## loop for multiple stocks

	for root,subdir,files in os.walk(stock_files_path):
		for i,f in enumerate(files):
			print ("processing %s ...%d out of %d" %(f,i,len(files)))

			file_path = os.path.join(stock_files_path,f)
			df = pd.read_csv(file_path)
			out = get_results(df)
			results_strategy.append(out)
	res_df = pd.concat(results_strategy)

	## allocating funds as per number of bids
	count_bids_daily = pd.DataFrame(res_df.Date.value_counts().reset_index())
	count_bids_daily.columns = ['Date', 'no_of_bids_per_day']
	df = pd.merge(res_df,count_bids_daily,on ='Date')
	df['funds_allocated'] = amount/df['no_of_bids_per_day']
	df['p_l'] = df['g_l'] * df['funds_allocated']
	df['right_bids'] = df['g_l'] > 0
	df['wrong_bids'] = df['g_l'] < 0

	df.to_csv('momentum_resultsv2.csv')
	plot_results(df)


def plot_results(data):
    data['Date'] = pd.to_datetime(data['Date'],format='%Y-%m-%d')
    df_plot = data.set_index('Date')
    df_plot = df_plot[['p_l','g_l','right_bids','wrong_bids']]

	#2017
    df_2017 = df_plot['2017']
    daily_df = df_2017.dropna(how='any').resample('D').sum()
    monthly_df = df_2017.dropna(how='any').resample('M').sum()

    daily_df.to_csv('mom_daily.csv')
    monthly_df.to_csv('mom_mon.csv')
   





if __name__=='__main__':
	main()