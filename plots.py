import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
from multiprocessing import Process, Queue


def plotCandlestick(xf: pd.DataFrame, title, q:Queue):
    plt.ion = True
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    # plt.xticks(rotation=30, ha='right')

    coldn = "red"
    colup = "green"
    width = (xf.index[1] - xf.index[0]) * 0.6
    width2 = width * 0.3
    ax.set_xlim(xf.index[0], xf.index[-1])
    
    plt.pause(.25)
    
    while True:
        df = q.get()
        up = df[df.Close >= df.Open]
        down = df[df.Close < df.Open]

        ax.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=colup)
        ax.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=colup)
        ax.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=colup)

        ax.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=coldn)
        ax.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color=coldn)
        ax.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color=coldn)
        
        plt.pause(.25)

    # plt.show()


def plotProcess(df: pd.DataFrame, title=None):
    process = Process(target=plotCandlestick, args=(df, title))
    process.start()


