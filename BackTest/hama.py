import pandas as pd

class HAMACalculator:
    def __init__(self, period):
        self.period = period
        self.ha_open = None
        self.ha_close = None
        self.hama = None

    def update(self, new_bar):
        """
        Update HAMA values with a new OHLC bar.

        Parameters:
        - new_bar: Dictionary with 'Date', 'Open', 'High', 'Low', 'Close' keys.
        """
        if self.ha_open is None:
            self.ha_open = new_bar['Open']
            self.ha_close = new_bar['Close']
            self.hama = 0.0
        else:
            self.ha_open = (self.ha_open + self.ha_close) / 2
            self.ha_close = (new_bar['Open'] + new_bar['High'] + new_bar['Low'] + new_bar['Close']) / 4
            self.hama = self.ha_close - pd.Series.rolling(self.ha_open, window=self.period).mean()

    def get_values(self):
        """
        Get the current HAMA values.

        Returns:
        - Dictionary with 'HA_Open', 'HA_Close', 'HAMA' keys.
        """
        return {'HA_Open': self.ha_open, 'HA_Close': self.ha_close, 'HAMA': self.hama}

# Example usage:
# Create an instance of HAMACalculator with the desired period.
hama_calculator = HAMACalculator(period=9)

# Simulate updating HAMA values as new OHLC bars arrive.
new_bars = [
    {'Date': '2023-01-01', 'Open': 100, 'High': 110, 'Low': 90, 'Close': 105},
    # Add more bars as needed
]

for bar in new_bars:
    hama_calculator.update(bar)
    hama_values = hama_calculator.get_values()
    print(f"Date: {bar['Date']}, HAMA Values: {hama_values}")
