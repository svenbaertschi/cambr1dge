import csv, io
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
import xlsxwriter
import pandas as pd
import numpy as np
import datetime
import pandas_datareader
import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from econometrica.models import effFrontier


# Create your views here.

# one parameter named request
def upload_csv(request):
	# declaring template
	template = "econometrica/upload.html"
	# GET request returns the value of the data with the specified key.
	if request.method == "GET":
		return render(request, template)
	csv_file = request.FILES['file']
# Read in price data
	df = pd.read_csv(csv_file, parse_dates=True, index_col="date")

# Calculate expected returns and sample covariance
	mu = df.mean()
	S = df.cov()
	print(mu, S)
# Optimise for maximal Sharpe ratio
	ef = EfficientFrontier(mu, S)

	#Max Sharpe
	raw_weights = ef.max_sharpe()
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	df1 = pd.DataFrame(efgdamn, index = ['values'])
	df2 = pd.DataFrame(cleaned_weights, index = ['weights'])
	dfmaxsharpe = pd.concat([df1, df2], axis=1)

	#minVar
	raw_weights = ef.min_volatility()
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	df1 = pd.DataFrame(efgdamn, index = ['values'])
	df2 = pd.DataFrame(cleaned_weights, index = ['weights'])
	dfminvar = pd.concat([df1, df2], axis=1)

	#frontier
	min_mu = min(mu)
	max_mu = max(mu)

	raw_weights = ef.efficient_return(min_mu)
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	efgdamn = {**efgdamn, **cleaned_weights}
	dfportfolios = pd.DataFrame(efgdamn, index = [1])

	while (min_mu <= max_mu):
		raw_weights = ef.efficient_return(min_mu)
		cleaned_weights = ef.clean_weights()
		efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
		efgdamn = {**efgdamn, **cleaned_weights}
		aaawtf = pd.DataFrame(efgdamn, columns = dfportfolios.columns, index= [1]) 
		dfportfolios = dfportfolios.append(aaawtf)
		min_mu +=max_mu*0.01

	try:
		from io import BytesIO as IO
	except ImportError:
		from io import StringIO as IO
    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
	excel_file = IO()
	xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
	dfmaxsharpe.to_excel(xlwriter, 'MaxSharpe')
	dfminvar.to_excel(xlwriter, 'MinVar')
	dfportfolios.to_excel(xlwriter, 'FrontierPortfolios')

	xlwriter.save()
	xlwriter.close()

    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
	excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
	response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
	response['Content-Disposition'] = 'attachment; filename=econometrica-results.xlsx'
	return response

def stocksaction(request, start, end, periodicity, tickers):
    yf.pdr_override()

    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")

    df = yf.download(tickers.split(" "), start = start, end = end, interval = periodicity)
    
    try:
        from io import BytesIO as IO # for modern python
    except ImportError:
        from io import StringIO as IO # for legacy python
    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
    excel_file = IO()

    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    df.to_excel(xlwriter, 'stockdata')

    xlwriter.save()
    xlwriter.close()

    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=cambr1dge-stock-data.xlsx'

    return response