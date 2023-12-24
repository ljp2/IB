import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import MultiCursor

import pandas as pd
from multiprocessing import Process, Queue
import platform


class Plot:
    def __init__(self, df: pd.DataFrame, title="Plot Process") -> None:
        self.df = df
        self.candles = []
        self.ha = []
        self.i_last = len(df) - 1
        self.i_left = 0
        self.i_width = 30
        self.i_delta = 5
        self.i_right = self.i_left + self.i_width
        
        self.dfleft = self.df.index[0]
        self.dfright = self.df.index[self.i_last]
        self.dfhigh = self.df.High.max()
        self.dflow = self.df.Low.min()

        self.x_left = self.df.index[self.i_left]
        self.x_right = self.df.index[self.i_right]
        self.y_high = self.dfhigh
        self.y_low = self.dflow

        self.width = (self.df.index[1] - self.df.index[0]) * 0.6
        self.width2 = self.width * 0.1

        # Create subplots with shared x-axis
        plt.ion = True
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, sharex=True, sharey=True)

        # Set titles
        self.fig.suptitle(title)
        self.ax1.set_title("Candles")
        self.ax2.set_title("HA")
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax1.yaxis.tick_right()
        self.ax2.yaxis.tick_right()

        # set axes limits .. remember x and y are shared
        self.setXlimits(self.x_left, self.x_right)
        self.ax1.set_ylim(self.y_low, self.y_high)
        self.ax2.set_ylim(self.y_low, self.y_high)

        self.multi = MultiCursor(None, (self.ax1, self.ax2), color="r", lw=1)

        plt.pause(0.25)
        
    def setXlimits(self, left, right):
        self.ax1.set_xlim(left, right)
        self.ax2.set_xlim(left, right)

    def addCandle(self, bardf: pd.DataFrame):
        if (bardf.Close >= bardf.Open).any():
            self.ax1.bar(
                bardf.index,
                bardf.Close - bardf.Open,
                self.width,
                bottom=bardf.Open,
                color="green",
            )
            self.ax1.bar(
                bardf.index,
                bardf.High - bardf.Close,
                self.width2,
                bottom=bardf.Close,
                color="green",
            )
            self.ax1.bar(
                bardf.index,
                bardf.Low - bardf.Open,
                self.width2,
                bottom=bardf.Open,
                color="green",
            )
        else:
            self.ax1.bar(
                bardf.index,
                bardf.Close - bardf.Open,
                self.width,
                bottom=bardf.Open,
                color="red",
            )
            self.ax1.bar(
                bardf.index,
                bardf.High - bardf.Open,
                self.width2,
                bottom=bardf.Open,
                color="red",
            )
            self.ax1.bar(
                bardf.index,
                bardf.Low - bardf.Close,
                self.width2,
                bottom=bardf.Close,
                color="red",
            )


    def addHA(self, bardf: pd.DataFrame):
        pass
    
    
    def addBar(self, bardf: pd.DataFrame):
        # if bardf.index[0] >= self.x_right:
        #     self.i_left += self.i_delta
        #     self.i_right = min(self.i_right + self.i_delta, self.i_last)
        #     self.x_left = self.df.index[self.i_left]
        #     self.x_right = self.df.index[self.i_right]
        #     self.setXlimits(self.x_left, self.x_right)
        self.addCandle(bardf=bardf)
        self.addHA(bardf=bardf)

        plt.draw()
        plt.pause(0.1)


class PlotProcess(Process):
    def __init__(self, df: pd.DataFrame) -> None:
        # self.df = df
        super().__init__(target=self.plotCandlesHA, args=(df,))
        self.daemon = True
        self.i: int = 0
        self.q: Queue = Queue()
        self.daemon = True
        self.start()

    def plotCandlesHA(self, df):
        self.candlesHA_plot = Plot(df)
        while True:
            bardf = self.q.get()
            self.candlesHA_plot.addBar(bardf=bardf)


if __name__ == "__main__":
    barfilename = "20231130"
    filedirectory = "~/Data" if platform.system() == "Darwin" else "c:/Data"
    filepath = f"{filedirectory}/{barfilename}.csv"
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

    plot_process = PlotProcess(df)

    import arrivals
    arrivals = arrivals.Arrivals(df)

    while arrivals.waitforarrival() is not None:
        newbar = arrivals.arrival
        plot_process.q.put(newbar)
 
