import matplotlib.pyplot as plt
from matplotlib import axes
import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import time
from multiprocessing import Process, Queue
import platform

import plots

class ArrivalIterator:
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.df):
            result = self.df.iloc[[self.index]]
            self.index += 1
            return result
        else:
            raise StopIteration



class PlotProcess:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.i:int =0
        self.q:Queue = Queue()
        plot_process = Process(target=self.plotProcess, args=(df, self.q))
        plot_process.daemon = True
        plot_process.start()

    def plotProcess(self, df: pd.DataFrame, title=""):
        plots.plotCandlestick(self.df, title="From Trade", q=self.q)
        
    def addBar(self, bardf:pd.DataFrame):
        self.q.put(bardf)


def initialize(df:pd.DataFrame):
    plot_process = PlotProcess(df)
    return plot_process


def waitforarrival(df:pd.DataFrame, plot_process:PlotProcess):
    plot_process.q.put(df)
    


def analyze():
    pass


def plot(p:PlotProcess):
    p.q.put('something')


def decide():
    pass


def summarize():
    pass


def main():
    barfilename = "20231130.csv"
    filedirectory = '~/Data' if platform.system()=='Darwin' else 'c:/Data'
    filepath = f'{filedirectory}/{barfilename}'
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    plot_process = initialize(df)
    arrivals = ArrivalIterator(df)
    
    for newbar in arrivals:
        plot_process.addBar(newbar)
        analyze()
        decide()
        summarize()
        time.sleep(0.25)
        
        

if __name__ == "__main__":
    main()
