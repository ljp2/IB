import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import MultiCursor

import pandas as pd
from multiprocessing import Process, Queue

class Plot():
    def __init__(self, df:pd.DataFrame, title) -> None:
        plt.ion = True
        
        x_min = df.index[0]
        x_max = df.index[-1]
        y_high = df.High.max()
        y_low = df.Low.min()

        
        # Create subplots with shared x-axis
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
        
        # Set titles
        self.fig.suptitle(title)
        self.ax1.set_title('Candles')
        self.ax2.set_title('HA')
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax1.yaxis.tick_right()
        self.ax2.yaxis.tick_right()
        
        # set axes limits .. remember x and y are shared
        self.ax1.set_xlim(x_min, x_max)  
        self.ax1.set_ylim(y_low, y_high)  
        self.ax2.set_xlim(x_min, x_max)  
        self.ax2.set_ylim(y_low, y_high)  
        

        self.multi = MultiCursor(None, (self.ax1, self.ax2), color='r', lw=1)
        

        plt.show()
        
        
        


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

class PlotProcess:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.i: int = 0
        self.q: Queue = Queue()
        plot_process = Process(target=self.plotProcess, args=(df, self.q))
        plot_process.daemon = True
        plot_process.start()

    def plotProcess(self, df: pd.DataFrame, title=""):
        plotCandlestick(self.df, title="From Trade", q=self.q)

    def addBar(self, bardf: pd.DataFrame):
        self.q.put(bardf)


def plotCandlestick(df: pd.DataFrame, title, q:Queue):
    candlestick_plot = CandleStickPlot(df, title)
    while True:
        bardf = q.get()
        candlestick_plot.addBar(bardf=bardf)


def plotProcess(df: pd.DataFrame, title=None):
    process = Process(target=plotCandlestick, args=(df, title))
    process.start()
