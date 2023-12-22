
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import MultiCursor

import pandas as pd
from multiprocessing import Process, Queue
import platform

class Plot():
    def __init__(self, df:pd.DataFrame, title='Plot Process') -> None:
        self.candles = []
        self.ha = []
        
        x_min = df.index[0]
        x_max = df.index[-1]
        y_high = df.High.max()
        y_low = df.Low.min()

        self.width = (df.index[1] - df.index[0]) * 0.6
        self.width2 = self.width * 0.3
        
        # Create subplots with shared x-axis
        plt.ion = True
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
    
        plt.pause(.25)
        
    def addCandle(self, bardf:pd.DataFrame):
        if (bardf.Close >= bardf.Open).any():
            self.ax1.bar(bardf.index, bardf.Close - bardf.Open, self.width, bottom=bardf.Open, color="green")
            self.ax1.bar(bardf.index, bardf.High - bardf.Close, self.width2, bottom=bardf.Close, color="green")
            self.ax1.bar(bardf.index, bardf.Low - bardf.Open,self. width2, bottom=bardf.Open, color="green")
        else:
            self.ax1.bar(bardf.index, bardf.Close - bardf.Open, self.width, bottom=bardf.Open, color= "red")
            self.ax1.bar(bardf.index, bardf.High - bardf.Open, self.width2, bottom=bardf.Open, color= "red")
            self.ax1.bar(bardf.index, bardf.Low - bardf.Close, self.width2, bottom=bardf.Close, color= "red")
            
    def addBar(self, bardf:pd.DataFrame):
        self.addCandle(bardf=bardf)
        
        plt.draw()
        plt.pause(.1)
    

# class PlotProcess:
#     def __init__(self, df: pd.DataFrame, q:Queue) -> None:
#         self.df = df
#         self.i: int = 0
#         self.q: Queue = Queue()
#         process = Process(target=self.plotProcess, args=(df,self.q))
#         process.daemon = True
#         process.start()

#     def plotProcess(self, df: pd.DataFrame):
#         self.plot:Plot = Plot(self.df, title="From Trade")

#     def addBar(self, bardf: pd.DataFrame):
#         self.plot.addCandle(bardf=bardf)

def plotCandlesHA(df: pd.DataFrame, q:Queue):
    candlesHA_plot = Plot(df)
    while True:
        bardf = q.get()
        candlesHA_plot.addBar(bardf=bardf)
        
def plotProcess(df: pd.DataFrame):
    q = Queue()
    process = Process(target=plotCandlesHA, args=(df, q))
    process.start()
    return q


if __name__ == "__main__":
    barfilename = '20231130'
    filedirectory = "~/Data" if platform.system() == "Darwin" else "c:/Data"
    filepath = f"{filedirectory}/{barfilename}.csv"
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    
    # plot_process = PlotProcess(df)
    
    
    input('WAITING')
    

