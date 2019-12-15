from django.db import models
import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Create your models here.
def effFrontier(data):


    # Read in price data
    df = pd.read_csv(data, parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = df.mean()
    S = df.cov()
    print(mu, S)
    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights.csv")  # saves to file

    ef.portfolio_performance(verbose=True)
    df1 = pd.DataFrame(ef.portfolio_performance(), index = ['mean', 'stdev', 'sharpe'])
    df2 = pd.DataFrame(cleaned_weights, index = ['weights'])
    return(df1)
