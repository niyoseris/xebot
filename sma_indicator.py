import requests


def sma_indicator(pair):
    # Function to calculate the Simple Moving Average (SMA)
    def calculate_sma(data, window_size):
        if len(data) < window_size:
            return None
        return sum(data[-window_size:]) / window_size

    # Initialize parameters
    url = f"https://api.xeggex.com/api/v2/cmctrades/{pair}_USDT"  # Replace with your API endpoint
    window_size = 10  # You can adjust this window size as needed

    # Initialize lists to store trade prices
    trade_prices = []

    try:
        # Fetch the data from the API
        response = requests.get(url)
        data = response.json()

        data.reverse()

        # Extract trade prices from the response
        prices = [float(trade['price']) for trade in data]

        # Append the new prices to the list
        trade_prices.extend(prices)

        # Calculate SMA
        sma = calculate_sma(trade_prices, window_size)

        # Calculate Spread
        if sma is not None:
            spread = trade_prices[-1] - sma
        else:
            spread = None

        if spread is not None:
            #print(f"Spread: {spread:.10f}")
            return f"{spread:.10f}"
        else:
            print("Not enough data to calculate Spread")

    except Exception as e:
        print(f"Error: {e}")

