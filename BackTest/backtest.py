# python backtest.py 2>&1 | sed '/Secure coding is not enabled for restorable state!/d'
import time
import platform
import pandas as pd
from multiprocessing import Process, Queue

import arrivals
import backtestplots as plots

import initialize


def analyze():
    pass


def decide():
    pass


def summarize():
    pass



if __name__ == "__main__":
    
    barfilename = '20231130'
    filedirectory = "~/Data" if platform.system() == "Darwin" else "c:/Data"
    filepath = f"{filedirectory}/{barfilename}.csv"
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    arrivals = arrivals.Arrivals(df)
    plot_process = plots.PlotProcess(df)

    while arrivals.waitforarrival() is not None:
        newbar = arrivals.arrival
        plot_process.q.put(newbar)
        analyze()
        decide()
        summarize()
    
    
    # input('WAITING\n')
