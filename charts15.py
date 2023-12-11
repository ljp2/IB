import pandas as pd 

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import mplfinance as mpf 
from datetime import datetime, time, timedelta
from multiprocessing import Process
import pandas_ta as ta 

def plotCandlestick(df:pd.DataFrame, title=""):
    fig, ax = plt.subplots()
    ax.set_title(title)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # plt.xticks(rotation=30, ha='right') 
    
    coldn = 'red'
    colup = 'green'
    width = (df.index[1] - df.index[0]) * 0.6
    width2 = width * 0.3

    up = df[df.Close >= df.Open] 
    down = df[df.Close < df.Open] 

    ax.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=colup) 
    ax.bar(up.index, up.High-up.Close, width2, bottom=up.Close, color=colup) 
    ax.bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color=colup) 

    ax.bar(down.index, down.Close-down.Open, width, bottom=down.Open, color=coldn) 
    ax.bar(down.index, down.High-down.Open, width2, bottom=down.Open, color=coldn) 
    ax.bar(down.index, down.Low-down.Close, width2, bottom=down.Close, color=coldn) 

    plt.show() 

def ohlc(df:pd.DataFrame, bar_index_first=True):
    """Reduces the dataframe to a single ohlc line

    Args:
        df (pd.DataFrame): the input dateframe with Open, Hign, Low, Close column names

    Returns:
        pd.DataFrame: frame consists of one record with Open, Hign, Low, Close column names
    """
    index = df.index[0] if bar_index_first else df.index[-1]
    x = [{
        'Open' : df.Open.iloc[0],
        'High' : df.High.max(),
        'Low' : df.Low.min(),
        'Close' : df.Close.iloc[-1]
    }]
    return pd.DataFrame(x, index=[index])


def reduceDF(df:pd.DataFrame, group_sz:int) -> pd.DataFrame:
    """Reduces the dataframe by combining groups of lines into singel ohlc lines.
    The lines are combined starting backward from end of dataframe.  Thus there may
    be some lines of the original dataframe that are not condsidered.

    Args:
        df (pd.DataFrame): the input dataframe with Open, Hign, Low, Close column names
        group_sz (int): the number of line that will be combined

    Returns:
        pd.DataFrame: the reduced dataframe with Open, Hign, Low, Close column names.
        The dataframe will have df.shape[0] // group_sz records.
    """    
    xf = pd.DataFrame()
    numdfrows = df.shape[0]
    ngroups = numdfrows // group_sz
    numtargetrows = ngroups * group_sz
   
    while start < numdfrows:
        end = start + group_sz
        xf = pd.concat(
            [xf, ohlc(df.iloc[start:end])]
        )
        start += group_sz
    return xf


def hybridDF(df:pd.DataFrame, group_sz:int) -> pd.DataFrame:
    """Produces a dataframe where each line of the original ohlc dataframe will
    be an ohlc line that was combinde from a previous number of lines inclusive of the current line.
    Note that the since the output dataframe will consider the last line of the input dataframe, it
    is possible that beginning lines of the input dataframe will not be considered.

    Args:
        df (pd.DataFrame): the input dataframe with Open, Hign, Low, Close column names.
        group_sz (int): the number of lines that will be combined for each original line 

    Returns:
        pd.DataFrame: the output  dataframe with Open, Hign, Low, Close column names.
    """    
    xf = pd.DataFrame()
    N = df.shape[0]
    start = 0
    end = start + group_sz
    while end <= N:
        xf = pd.concat(
            [xf, ohlc(df.iloc[start:end], False)]
        )
        start += 1
        end += 1
    return xf

def ha(df:pd.DataFrame):
    """Candle Type: Heikin Ashi"""
    # Validate Arguments
    open_ = df['Open']
    high =df['High']
    low = df['Low']
    close = df['Close']

    # Calculate Result
    m = close.size
    hf = pd.DataFrame({
        "Open": 0.5 * (open_.iloc[0] + close.iloc[0]),
        "High": high,
        "Low": low,
        "Close": 0.25 * (open_ + high + low + close),
    })

    for i in range(1, m):
        hf["Open"].iloc[i] = 0.5 * (hf["Open"].iloc[i - 1] + hf["Close"].iloc[i - 1])

    hf["High"] = hf[["Open", "High", "Close"]].max(axis=1)
    hf["Low"] = hf[["Open", "Low", "Close"]].min(axis=1)

    # Name and Categorize it
    # hf.name = "Heikin-Ashi"
    # hf.category = "candles"

    return hf

# def PlotCandles(df:pd.DataFrame, title="", addplot=None):
#     if addplot is not None:
#         mpf.plot(df, type='candle', style='charles', title=title, addplot=addplot)
#     else:
#         mpf.plot(df, type='candle', style='charles', title=title)



# if __name__ == "__main__":
#     df:pd.DataFrame = pd.read_csv('~/Data/20231130.csv', index_col=0, parse_dates=True)

#     # df = df.iloc[:11]
#     rf = reduceDF(df, 5)
#     hf = hybridDF(df,5)

#     hf['row_number'] = hf.reset_index().index
#     xf = hf[hf.row_number % 5 == 0]

#     plots = []
#     for i in range(5):
#         d = hf[hf.row_number % 5 == i]
#         plots.append(Process(target=PlotCandles, args=(d, f'hf - {i}')))

#     for pi in plots:
#         pi.start()
#         # pi.join()
       

if __name__ == "__main__":
    df:pd.DataFrame = pd.read_csv('c:/Data/20231130.csv', index_col=0, parse_dates=True)
    hf = hybridDF(df,5)
    # Get the current date
    current_date = hf.index[0]
    start = datetime.combine(current_date, time(9,30))

    ds = [pd.DataFrame() for i in range(5)]

    for index, row in hf.iterrows():
        i = (index - start).seconds // 60 % 5
        ds[i] = pd.concat([ds[i], row.to_frame().transpose()])

    for i in range(5):
        h = ha(ds[i])
        Process(target=plotCandlestick, args=(h, f'plot - {i}')).start()
        # plotCandlestick(h, "test")
        


    # apmavs = [ mpf.make_addplot(df.Close)]
              
    # # PlotCandles(df,'a;sdfjk')
    # # mpf.plot(xf, type='candle', style='charles',
    # #          addplot=apmavs)

    # ap = [ mpf.make_addplot(df.Close)]
    # hap = [ mpf.make_addplot(df.loc[hf.index[0]:hf.index[-1]].Close)]
    
    
    # p1 = Process(target=PlotCandles, args=(df, 'df', ap))
    # p2 = Process(target=PlotCandles, args=(rf, 'reduce'))
    # # p3 = Process(target=PlotCandles, args=(hf, 'hybrid', hap))
    # p3 = Process(target=PlotCandles, args=(xf, 'hybrid-5'))

    # p1.start()
    # p2.start()
    # p3.start()
    # p1.join()
    # p2.join()
    # p3.join()
    