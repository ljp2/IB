import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import MultiCursor
from matplotlib.axes import Axes

import pandas as pd
from multiprocessing import Process, Queue
import platform


class Plot:
    def __init__(self, df: pd.DataFrame, title="Plot Process") -> None:
        self.df = df
        self.bars = pd.DataFrame()
        self.habars = pd.DataFrame()
        self.current_i = 0
        self.i_last = len(df) - 1
        self.i_left = 0
        self.i_width = 389
        self.i_plot_shift_delta = 5
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

    def plotBar(self, bardf: pd.DataFrame, ax:Axes):
        """Plots the bar directory on the candles (the upper) subplot

        Args:
            bardf (pd.DataFrame): a classic OHLCV bar
        """
        if (bardf.Close >= bardf.Open).any():
            ax.bar(
                bardf.index,
                bardf.Close - bardf.Open,
                self.width,
                bottom=bardf.Open,
                color="green",
            )
            ax.bar(
                bardf.index,
                bardf.High - bardf.Close,
                self.width2,
                bottom=bardf.Close,
                color="green",
            )
            ax.bar(
                bardf.index,
                bardf.Low - bardf.Open,
                self.width2,
                bottom=bardf.Open,
                color="green",
            )
        else:
            ax.bar(
                bardf.index,
                bardf.Close - bardf.Open,
                self.width,
                bottom=bardf.Open,
                color="red",
            )
            ax.bar(
                bardf.index,
                bardf.High - bardf.Open,
                self.width2,
                bottom=bardf.Open,
                color="red",
            )
            ax.bar(
                bardf.index,
                bardf.Low - bardf.Close,
                self.width2,
                bottom=bardf.Close,
                color="red",
            )

    def getHAbar(self, bardf: pd.DataFrame):
        """calculates the next (or first) heiken-ashi bar and then plots it on ha (the lower plot.)

        Args:
            bardf (pd.DataFrame): the recently arrived OHLCV bar
        """
        if len(self.habars) == 0:
            hadf = self.calculate_first_heiken_ashi(bardf)
        else:
            hadf = self.calculate_next_heiken_ashi(bardf)
        return hadf

    def calculate_first_heiken_ashi(self, df: pd.DataFrame):
        df["HA_Close"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
        df["HA_Open"] = df["Open"]
        df["HA_High"] = df[["High", "HA_Open", "HA_Close"]].max(axis=1)
        df["HA_Low"] = df[["Low", "HA_Open", "HA_Close"]].min(axis=1)
        heiken_ashi_df = df[["HA_Open", "HA_High", "HA_Low", "HA_Close"]]
        heiken_ashi_df.columns = ["Open", "High", "Low", "Close"]
        return heiken_ashi_df

    def calculate_next_heiken_ashi(self, new_ohlc_candle: pd.DataFrame
    ):
        previous_ha_candle = self.habars.iloc[-1]
        previous_ha_open, previous_ha_close = previous_ha_candle[["Open", "Close"]]
        new_open, new_high, new_low, new_close = new_ohlc_candle[["Open", "High", "Low", "Close"]].iloc[0]
        ap = (new_open + new_high + new_low + new_close) / 4
        ha_open = (previous_ha_open + previous_ha_close) / 2
        ha_high = max(new_open, new_close, new_high, ha_open)
        ha_low = min(new_open, new_close, new_low, ha_open)
        ha_close = (ap + ha_open + ha_high + ha_low) / 4

        data_list = [ha_open, ha_high, ha_low, ha_close]
        heiken_ashi_df = pd.DataFrame(
            [data_list],
            index=new_ohlc_candle.index,
            columns=["Open", "High", "Low", "Close"],
        )
        return heiken_ashi_df

    def addBar(self, bardf: pd.DataFrame):
        self.bars = pd.concat([self.bars, bardf])
        self.plotBar(bardf=bardf, ax=self.ax1)
        
        habardf = self.getHAbar(bardf=bardf)
        self.habars = pd.concat([self.habars, habardf])
        self.plotBar(bardf=habardf, ax=self.ax2)
        plt.draw()
        plt.pause(0.1)


class PlotProcess(Process):
    def __init__(self, df: pd.DataFrame) -> None:
        self.i: int = 0
        self.q: Queue = Queue()
        super().__init__(target=self.plotCandlesHA, args=(df,))
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
