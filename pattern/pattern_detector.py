import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PatternDetector():
    def __init__(self) -> None:
        pass

class VCPDetector(PatternDetector):
    def __init__(self) -> None:
        super().__init__()

    def calculate_vcp(self, stock_data, window=50):
        stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()
        stock_data['Volume_SMA'] = stock_data['Volume'].rolling(window=window).mean()
        
        stock_data['Volatility'] = stock_data['Close'].rolling(window=window).std()
        stock_data['Volatility_Contraction'] = stock_data['Volatility'].rolling(window=window).mean()
        
        stock_data['Volume_Contraction'] = stock_data['Volume'].rolling(window=window).mean()
        
        return stock_data

    def detect_vcp(self,stock_data):
        vcp_signals = []
        for i in range(1, len(stock_data)):
            if (stock_data['Volatility_Contraction'].iloc[i] < stock_data['Volatility_Contraction'].iloc[i-1] and
                stock_data['Volume_Contraction'].iloc[i] < stock_data['Volume_Contraction'].iloc[i-1]):
                vcp_signals.append(stock_data.index[i])
        return vcp_signals

    def plot_vcp(self,stock_data, vcp_signals):
        plt.figure(figsize=(14, 7))
        plt.plot(stock_data['Close'], label='Close Price')
        plt.plot(stock_data['SMA'], label='50-day SMA', linestyle='--')
        
        for signal in vcp_signals:
            plt.axvline(signal, color='r', linestyle='--', alpha=0.7)
        
        plt.title('Volatility Contraction Pattern (VCP) Detection')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
