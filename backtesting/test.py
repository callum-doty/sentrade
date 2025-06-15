import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load historical stock data
ticker = "AAPL"
df = yf.download(ticker, start="2020-01-01", end="2025-01-01")
#df = df[['Close']].copy()

