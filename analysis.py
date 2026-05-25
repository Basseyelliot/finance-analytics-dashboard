import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from prophet import Prophet


def get_stock_data(ticker="KO", start="2025-01-01", end="2025-12-31"):
    df = yf.download(ticker, start=start, end=end, auto_adjust=False)

    if isinstance(df.columns, pd.MultiIndex):
        df = df["Close"]
        df.columns = ["Close Price"]
    else:
        df = df[["Close"]]
        df.columns = ["Close Price"]

    return df.dropna()


def plot_stock_price():
    df = get_stock_data()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close Price"], label="Close Price")
    ax.set_title("KO Stock Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()

    return fig


def plot_moving_average():
    df = get_stock_data()
    df["SMA_20"] = df["Close Price"].rolling(window=20).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["Close Price"], label="Close Price")
    ax.plot(df.index, df["SMA_20"], label="20-Day Moving Average")
    ax.set_title("Moving Average Analysis")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.legend()

    return fig


def run_monte_carlo():
    df = get_stock_data()

    returns = df["Close Price"].pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()

    num_simulations = 100
    num_days = 30
    last_price = df["Close Price"].iloc[-1]

    simulation_results = np.zeros((num_days, num_simulations))

    for i in range(num_simulations):
        prices = [last_price]

        for t in range(num_days):
            random_shock = np.random.normal(mu, sigma)
            next_price = prices[-1] * (1 + random_shock)
            prices.append(next_price)

        simulation_results[:, i] = prices[1:]

    final_prices = simulation_results[-1]

    summary = {
        "Mean Forecast Price": round(final_prices.mean(), 2),
        "Minimum Forecast Price": round(final_prices.min(), 2),
        "Maximum Forecast Price": round(final_prices.max(), 2),
    }

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    for i in range(num_simulations):
        ax1.plot(simulation_results[:, i], alpha=0.4)

    ax1.set_title("Monte Carlo Simulation - 30 Day Forecast")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Forecast Price")
    ax1.grid(True)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.hist(final_prices, bins=20)
    ax2.set_title("Distribution of Final Prices")
    ax2.set_xlabel("Price")
    ax2.set_ylabel("Frequency")
    ax2.grid(True)

    return summary, fig1, fig2


def run_prophet_forecast():
    raw_df = yf.download("KO", period="5y", auto_adjust=False)
    raw_df = raw_df.reset_index()

    if isinstance(raw_df.columns, pd.MultiIndex):
        raw_df.columns = [
            col[0] if col[0] != "" else col[1]
            for col in raw_df.columns
        ]

    if "Close" not in raw_df.columns and "Adj Close" in raw_df.columns:
        raw_df["Close"] = raw_df["Adj Close"]

    prophet_df = raw_df[["Date", "Close"]].copy()

    prophet_df = prophet_df.rename(columns={
        "Date": "ds",
        "Close": "y"
    })

    prophet_df = prophet_df.dropna()

    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=165)
    forecast = model.predict(future)

    fig1 = model.plot(forecast)
    plt.title("Facebook Prophet Forecast for KO Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Closing Stock Price")

    fig2 = model.plot_components(forecast)

    forecast_table = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10)

    return forecast_table, fig1, fig2