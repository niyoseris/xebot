import requests
import numpy as np

def get_rsi(coinVusdt, last, period):

    def fetch_candle_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            candle_data = data.get("bars", [])
            return [candle["close"] for candle in candle_data]
        else:
            return None

    def calculate_rsi(prices, period=14):
        # Fiyat değişikliklerini hesapla
        price_diff = np.diff(prices)

        # Artan ve azalan fiyat değişikliklerini ayrı ayrı hesapla
        gain = np.where(price_diff > 0, price_diff, 0)
        loss = np.where(price_diff < 0, -price_diff, 0)

        # Ortalama artan ve azalan değişiklikleri hesapla
        avg_gain = np.mean(gain[:period])
        avg_loss = np.mean(loss[:period])

        rs_values = []
        rsi_values = []

        for price in price_diff[period:]:
            avg_gain = ((avg_gain * (period - 1)) + max(price, 0)) / period
            avg_loss = ((avg_loss * (period - 1)) + max(-price, 0)) / period
            rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
            rsi = 100 - (100 / (1 + rs))
            rs_values.append(rs)
            rsi_values.append(rsi)
        

        if len(rsi_values) > last - 16:
            return rsi_values[last-16]
        else:
            return False
        
    # Verileri çekmek istediğiniz URL
    url = f"https://api.xeggex.com/api/v2/market/candles?symbol={ coinVusdt }%2FUSDT&resolution={period}&countBack={last}&firstDataRequest=1"

    # Verileri çek
    prices = fetch_candle_data(url)

    if prices:
        rsi_values = calculate_rsi(prices, period=14)
        return (rsi_values)
    else:
        return ("Veri çekme hatası!")
