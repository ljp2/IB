import pandas as pd 
import matplotlib.pyplot as plt
import mplfinance as mpf 

from multiprocessing import Process

def ohlc(df:pd.DataFrame):
    x = [{
        'Open' : df.Open.iloc[0],
        'High' : df.High.max(),
        'Low' : df.Low.min(),
        'Close' : df.Close.iloc[-1]
    }]
    return pd.DataFrame(x, index=[df.index[0]])


def combineDF(df:pd.DataFrame, group_sz:int) -> pd.DataFrame:
    xf = pd.DataFrame()
    numdfrows = df.shape[0]
    ngroups = numdfrows // group_sz
    numtargetrows = ngroups * group_sz
    start = numdfrows - numtargetrows
    while start < numdfrows:
        end = start + group_sz
        xf = pd.concat(
            [xf, ohlc(df.iloc[start:end])]
        )
        start += group_sz
    return xf


def multibars(df:pd.DataFrame, group_sz:int) -> pd.DataFrame:
    xf = pd.DataFrame()
    N = df.shape[0]
    start = 0
    end = start + group_sz
    while end <= N:
        xf = pd.concat(
            [xf, ohlc(df.iloc[start:end])]
        )
        start += 1
        end += 1
    return xf



def PlotCandles(df:pd.DataFrame):
    mpf.plot(df, type='candle', style='charles')

def main():
    df:pd.DataFrame = pd.read_csv('~/Data/20231130.csv', index_col=0, parse_dates=True)
    # xf = combineDF(df, 5)

    xf = multibars(df,5)

    p1 = Process(target=PlotCandles, args=(df,))
    p2 = Process(target=PlotCandles, args=(xf,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()