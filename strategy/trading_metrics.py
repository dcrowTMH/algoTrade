import numpy as np
import pandas as pd

class TradingMetric():
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> None:
        pass

    # daily return rate
    def daily_return_rate(self, daily_data: pd.DataFrame) -> pd.Series:
        """
        function to simplify pulling the adjusted closed price from the dataset to calculate the
        daily return rate

        Arg:
            daily_data: pandas.DataFrame
                DataFrame Contains the adjusted closed price for the stock
        Returns:
        TODO: Fill the explaination
            pandas.Series

        """
        return daily_data['Adj Close'].pct_change()
    
    # annualized percent return
    def apr(self, daily_return: pd.Series, td: bool = True) -> float:
        """
        function used to calculate the annualized percent return
        Args:
            daily_return: pandas.Series
                daily adjusted close price data sorted by date & only the price value included
            td : bool
                Using 252 trading days/ standardization 365 days for calculation    
        
        Returns:
            float
                annualized rate of return
        """
        # assign the day based on the trading day/ standarization
        days = 252 if td else 365
        daily_return = daily_return.loc[lambda x : x != 0]
        return np.prod(1 + daily_return) ** (days / len(daily_return)) - 1
    
    # Sharpe Ratio
    def sharpe(self, daily_return: pd.Series, risk_free_rate: float = 0.0) -> float:
        """
        function to calculate the sharpe ratio, risk free rate can be used to compare the portfolio
        returns against

        Arg:
            daily_return: pandas.Series
                daily adjusted close price data sorted by date & only the price value included
            risk_free_rate: float:
                rate to be substrated for portfolio returns against comparison
        """
        return np.sqrt(252) * (np.mean(daily_return) - risk_free_rate) / np.std(daily_return)
    
    def max_dd(self, ts):
        """
        Calculate the maximum drawdown and the maximum drawdown duration of a time series of returns.

        Parameters:
        ts (numpy array): Array of returns.

        Returns:
        tuple: A tuple containing:
            
        max_dd (float): The maximum drawdown.
        max_ddd (int): The maximum drawdown duration.
        i (int): The index at which the maximum drawdown occurs.
        """
        # Calculate cumulative returns
        cum_ret = np.cumprod(1 + ts) - 1

        # Initialize high water mark, drawdown, and drawdown duration arrays
        # high water mark: keeps track of the highest value reached by the cumulative returns up
        # up to each point in time
        high_water_mark = np.zeros(cum_ret.shape)
        draw_down = np.zeros(cum_ret.shape)
        draw_down_duration = np.zeros(cum_ret.shape)

        # Loop through the time series to calculate high water mark and drawdowns
        for t in np.arange(1, cum_ret.shape[0]):
            # Update high water mark
            high_water_mark[t] = np.maximum(high_water_mark[t - 1], cum_ret[t])
            # Calculate drawdown
            draw_down[t] = (1 + cum_ret[t]) / (1 + high_water_mark[t]) - 1
            # Update drawdown duration
            if draw_down[t] == 0:
                draw_down_duration[t] = 0
            else:
                draw_down_duration[t] = draw_down_duration[t - 1] + 1

        # Find the maximum drawdown and its index
        max_dd, i = np.min(draw_down), np.argmin(draw_down)
        # Find the maximum drawdown duration
        max_ddd = np.max(draw_down_duration)

        return max_dd, max_ddd, i