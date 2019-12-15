import csv, io
from django.http import HttpResponse
from django.shortcuts import render
import xlsxwriter
import pandas as pd
import numpy as np
import pandas_datareader
from analyst.procedures import *
from analyst.forms import Options


# Create your views here.

# # one parameter named request
def upload_csv(request):
	procedure = request.POST.get('procedure', False)
# declaring template
	template = "econometrica/upload.html"
	# GET request returns the value of the data with the specified key.
	if request.method == "GET":
		return render(request, template, {'form':Options})
	csv_file = request.FILES['file']
# Read in data
	try:
		df = pd.read_csv(csv_file, parse_dates=True, index_col=0)
	except:
		df = pd.read_excel(csv_file, parse_dates=True, index_col=0)
	
	##Perform our precedures
	if procedure == 'markowitz':
		output = markowitz_optimization(df)
	elif procedure == 'correlation':
		output = correlation(df)
	elif procedure == 'covariance':
		output = covariance(df)

	try:
		from io import BytesIO as IO
	except ImportError:
		from io import StringIO as IO
    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
	excel_file = IO()
	xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
	
	for key in output:
		output[key].to_excel(xlwriter, key)

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