from django.shortcuts import render
from stockprices.forms import PostForm
from django.http import HttpResponse
import requests
import json

# Create your views here.
def authentication():
	import time, uuid, urllib
	import hmac, hashlib
	from base64 import b64encode

	"""
	Basic info
	"""
	url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
	method = 'GET'
	app_id = 'ilFsEd7a'
	consumer_key = 'dj0yJmk9Vmw4Y1FteEh1cmp0JmQ9WVdrOWFXeEdjMFZrTjJFbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWRl'
	consumer_secret = '7caf8264fd4a7f8782ac1632a34e16afccff34ef'
	concat = '&'
	query = {'location': 'sunnyvale,ca', 'format': 'json'}
	oauth = {
		'oauth_consumer_key': consumer_key,
		'oauth_nonce': uuid.uuid4().hex,
		'oauth_signature_method': 'HMAC-SHA1',
		'oauth_timestamp': str(int(time.time())),
		'oauth_version': '1.0'
	}

	"""
	Prepare signature string (merge all params and SORT them)
	"""
	merged_params = query.copy()
	merged_params.update(oauth)
	sorted_params = [k + '=' + urllib.parse.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
	signature_base_str =  method + concat + urllib.parse.quote(url, safe='') + concat + urllib.parse.quote(concat.join(sorted_params), safe='')

	"""
	Generate signature
	"""
	composite_key = urllib.parse.quote(consumer_secret, safe='') + concat
	oauth_signature = b64encode(hmac.new(composite_key, signature_base_str, hashlib.sha1).digest())

	"""
	Prepare Authorization header
	"""
	oauth['oauth_signature'] = oauth_signature
	auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.items()])

	"""
	Send request
	"""
	url = url + '?' + urllib.parse.urlencode(query)
	request = urllib.request.Request(url)
	request.add_header('Authorization', auth_header)
	request.add_header('X-Yahoo-App-Id', app_id)
	response = urllib.request.urlopen(request).read()
	print(response)

def weather(request):
	authentication()
	if request.method=='POST':
		content = request.POST['location']
		form = PostForm(initial={'location':content})
		data = requests.get("https://weather-ydn-yql.media.yahoo.com/forecastrss?location="+content+"&format=json").json


		if data['query']['results']:
			effectiveroot = data['query']['results']['channel']
			locale = effectiveroot['location']
			condition = effectiveroot['item']['condition']
			forecast = effectiveroot['item']['forecast'][0]
			return render(request, 'weather/index.html', {'condition':condition, 'forecast':forecast, 'form':form, 'locale':locale} )
		else:
			return render(request, 'weather/unknownlocale.html', {'form':form} )
	else:
		content = 'Vancouver, CA'
		form = PostForm(initial={'location':'Vancouver, BC'})
		data = requests.get("https://weather-ydn-yql.media.yahoo.com/forecastrss?location="+content+"&format=json").json
		effectiveroot = data['query']['results']['channel']
		locale = effectiveroot['location']
		condition = effectiveroot['item']['condition']
		forecast = effectiveroot['item']['forecast'][0]
		return render(request, 'weather/index.html', {'condition':condition, 'forecast':forecast, 'locale':locale, 'form':form} )

def stocks(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            start = request.POST['start']
            end = request.POST['end']
            periodicity = request.POST['periodicity']
            tickers = request.POST['tickers']
            return stocksaction(request, start, end, periodicity, tickers)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'stockprices/index.html', {'form':form})



def stocksaction(request, start, end, periodicity, tickers):
    from datetime import datetime
    import xlsxwriter
    import pandas as pd
    import datetime
    import pandas_datareader
    import yfinance as yf
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

    df.to_excel(xlwriter, 'sheetname')

    xlwriter.save()
    xlwriter.close()

    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
    excel_file.seek(0)

    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=wzdata.xlsx'

    return response