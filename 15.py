import pandas as pd 
import matplotlib.pyplot as plt
import mplfinance as mpf 

from multiprocessing import Process

def ohlc(df:pd.DataFrame):
    """Reduces the dataframe to a single ohlc line

    Args:
        df (pd.DataFrame): the input dateframe with Open, Hign, Low, Close column names

    Returns:
        pd.DataFrame: frame consists of one record with Open, Hign, Low, Close column names
    """    
    x = [{
        'Open' : df.Open.iloc[0],
        'High' : df.High.max(),
        'Low' : df.Low.min(),
        'Close' : df.Close.iloc[-1]
    }]
    return pd.DataFrame(x, index=[df.index[0]])


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
    start = numdfrows - numtargetrows
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

    xf = hybridDF(df,5)


    apmavs = [ mpf.make_addplot(df.Close)]
              
    mpf.plot(xf, type='candle', style='charles',
             addplot=apmavs)


    # p1 = Process(target=PlotCandles, args=(df,))
    # p2 = Process(target=PlotCandles, args=(xf,))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

if __name__ == '__main__':
    main()