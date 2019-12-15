def markowitz_optimization(data):
	import pandas as pd
	import numpy as np
	from pypfopt.efficient_frontier import EfficientFrontier
	from pypfopt import risk_models
	from pypfopt import expected_returns

# Calculate expected returns and sample covariance
	mu = data.mean()
	S = data.cov()

# Optimise for maximal Sharpe ratio
	ef = EfficientFrontier(mu, S)

	#Max Sharpe
	raw_weights = ef.max_sharpe()
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	df1 = pd.DataFrame(efgdamn, index = ['values'])
	df2 = pd.DataFrame(cleaned_weights, index = ['weights'])
	MaxSharpe = pd.concat([df1, df2], axis=1)

	#minVar
	raw_weights = ef.min_volatility()
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	df1 = pd.DataFrame(efgdamn, index = ['values'])
	df2 = pd.DataFrame(cleaned_weights, index = ['weights'])
	MinVar = pd.concat([df1, df2], axis=1)

	#frontier
	min_mu = min(mu)
	max_mu = max(mu)

	raw_weights = ef.efficient_return(min_mu)
	cleaned_weights = ef.clean_weights()
	efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
	efgdamn = {**efgdamn, **cleaned_weights}
	EfficientFrontier = pd.DataFrame(efgdamn, index = [1])

	while (min_mu <= max_mu):
		raw_weights = ef.efficient_return(min_mu)
		cleaned_weights = ef.clean_weights()
		efgdamn = {"mean":ef.portfolio_performance()[0], "stdev":ef.portfolio_performance()[1], "sharpe":ef.portfolio_performance()[2]}
		efgdamn = {**efgdamn, **cleaned_weights}
		aaawtf = pd.DataFrame(efgdamn, columns = EfficientFrontier.columns, index= [1]) 
		EfficientFrontier = EfficientFrontier.append(aaawtf)
		min_mu +=max_mu*0.01
	
	return {"MaxSharpe":MaxSharpe, "MinVar":MinVar, "EfficientFrontier":EfficientFrontier}

def correlation(data):
	import pandas as pd
	import numpy as np

	return {"Correlations":pd.DataFrame(data.corr(method='pearson'))}

def covariance(data):
	import pandas as pd

	return{'Covariances':pd.DataFrame(data.cov())}