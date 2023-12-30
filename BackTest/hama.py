import platform
import pandas as pd
from pandas import DataFrame as DF
from utils import ExponentialSmoothing as ES
from ha import HA

class HAMA:
    def __init__(self) -> None:
        self.ha = HA()
        self.ohlcbars = DF()
        self.smooth_ohlcbars = DF()
        self.hamabars = DF()
        
        self.periodOpen = 5
        self.periodHigh = 5
        self.periodLow = 5
        self.periodClose = 5
        
        self.exOpen = ES(self.periodOpen)
        self.exHigh = ES(self.periodHigh)
        self.exLow = ES(self.periodLow)
        self.exClose = ES(self.periodClose)
        
        
    def addBar(self, ohlcbar:DF):
        self.ohlcbars = pd.concat([self.ohlcbars, ohlcbar])
        O,H,L,C,_ = ohlcbar.iloc[0].values
        nO = self.exOpen.update(O)
        nH = self.exOpen.update(H)
        nL = self.exOpen.update(L)
        nC = self.exOpen.update(C)
        smooth_olhc_bar =  pd.DataFrame([[nO,nH,nL,nC]], index=ohlcbar.index,  columns=["Open", "High", "Low", "Close"] )
        new_hama_bar = self.ha.addBar(smooth_olhc_bar)
        return new_hama_bar
        
import arrivals
if __name__ == "__main__":
    barfilename = "20231130"
    filedirectory = "~/Data" if platform.system() == "Darwin" else "c:/Data"
    filepath = f"{filedirectory}/{barfilename}.csv"
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    arrivals = arrivals.Arrivals(df)
    hama = HAMA()

    while arrivals.waitforarrival() is not None:
        newbar = arrivals.arrival
        newhamabar = hama.addBar(newbar)
        print(newhamabar)
        
   
