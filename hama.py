import pandas as pd
from pandas import DataFrame as DF

class HAMA:
    def __init__(self) -> None:
        self.ohlcbars = DF()
        self.smooth_ohlcbars = DF()
        self.hamabars = DF()
        
        self.periodOpen = 5
        self.periodHigh = 5
        self.periodLow = 5
        self.periodClose = 5
        
    def addBar(self, ohlcbar:DF):
        self.ohlcbars = pd.concat(self.ohlcbars, ohlcbar)
        
        
    def smoothBars(self) -> None: