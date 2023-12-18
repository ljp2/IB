import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
from multiprocessing import Process, Queue

class CandleStickPlot():
    def __init__(self, df:pd.DataFrame, title) -> None:
        plt.ion = True
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        

        self.width = (df.index[1] - df.index[0]) * 0.6
        self.width2 = self.width * 0.3
        self.ax.set_xlim(df.index[0], df.index[-1])
        
        plt.pause(.25)
        
    def addBar(self, bardf:pd.DataFrame):
        if (bardf.Close >= bardf.Open).any():
            self.ax.bar(bardf.index, bardf.Close - bardf.Open, self.width, bottom=bardf.Open, color="green")
            self.ax.bar(bardf.index, bardf.High - bardf.Close, self.width2, bottom=bardf.Close, color="green")
            self.ax.bar(bardf.index, bardf.Low - bardf.Open,self. width2, bottom=bardf.Open, color="green")
        else:
            self.ax.bar(bardf.index, bardf.Close - bardf.Open, self.width, bottom=bardf.Open, color= "red")
            self.ax.bar(bardf.index, bardf.High - bardf.Open, self.width2, bottom=bardf.Open, color= "red")
            self.ax.bar(bardf.index, bardf.Low - bardf.Close, self.width2, bottom=bardf.Close, color= "red")
            
        plt.pause(.25)


def plotCandlestick(df: pd.DataFrame, title, q:Queue):
    candlestick_plot = CandleStickPlot(df, title)
    while True:
        bardf = q.get()
        candlestick_plot.addBar(bardf=bardf)


def plotProcess(df: pd.DataFrame, title=None):
    process = Process(target=plotCandlestick, args=(df, title))
    process.start()


