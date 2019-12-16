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
		min_mu +=max_mu*0.005
	
	return {"MaxSharpe":MaxSharpe, "MinVar":MinVar, "EfficientFrontier":EfficientFrontier}

def corrcov(data):
	import pandas as pd
	import numpy as np

	return {"Correlations":pd.DataFrame(data.corr(method='pearson')),'Covariances':pd.DataFrame(data.cov())}

def pca(data):
	import csv
	import pandas as pd
	from sklearn.preprocessing import StandardScaler
	from sklearn.decomposition import PCA

	data_scaled = StandardScaler().fit_transform(data)
	pca = PCA(n_components=data_scaled.shape[1])
	pca.fit_transform(data_scaled)

	explained_var = pca.explained_variance_ratio_
	explained_var_df = {}
	for i in range(0,len(explained_var)):
		explained_var_df["PC"+str(i+1)] = explained_var[i]
	explained_var_df = pd.DataFrame([explained_var_df], index=["Explained Var. Ratio"])

	values = pca.components_
	col_index = []
	for i in range(0,data.shape[1]):
		col_index.append("PC" + str(i+1))

	values_df = pd.DataFrame(values, columns = data.columns, index=col_index)
	return({'Principal Components':explained_var_df, 'Factor Loadings':values_df.transpose()})
