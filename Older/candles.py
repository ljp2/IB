import pandas as pd


def ohlc(df: pd.DataFrame, bar_index_first=True):
    """Reduces the dataframe df to a single ohlc line

    Args:
        df (pd.DataFrame): the input dateframe with Open, Hign, Low, Close column names

        bar_index_first (bool) True if the index of first record should be used.
        Otherwize index of last bar.

    Returns:
        pd.DataFrame: frame which consists of one record with Open, Hign, Low, Close column names
    """
    index = df.index[0] if bar_index_first else df.index[-1]
    x = [
        {
            "Open": df.Open.iloc[0],
            "High": df.High.max(),
            "Low": df.Low.min(),
            "Close": df.Close.iloc[-1],
        }
    ]
    return pd.DataFrame(x, index=[index])


def reduceDF(df: pd.DataFrame, group_sz: int) -> pd.DataFrame:
    """Reduces the dataframe by combining groups of group_sz ines into asingle ohlc lines.
    For example a df of 390 lines 1 min bars could be reduced to a df with 78 5 min bars.
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
    numtargetrows = ngroups * group_sz
    start = numdfrows - numtargetrows
    while start < numdfrows:
        end = start + group_sz
        xf = pd.concat([xf, ohlc(df.iloc[start:end])])
        start += group_sz
    return xf


def hybridDF(df: pd.DataFrame, group_sz: int) -> pd.DataFrame:
    """Produces a dataframe where each line of the original ohlc dataframe will
    be an ohlc line that was combinde from a group_sz number of lines ending with the current line.
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
        xf = pd.concat([xf, ohlc(df.iloc[start:end], False)])
        start += 1
        end += 1
    return xf


def ha(df: pd.DataFrame):
    """Produces a dataFrame of Heiken-Ashi candles from input dataframe of OHLC candles

    Args:
        df (pd.DataFrame): dataframe with columns Open, High, Low, Close

    Returns:
        pd.DataFame: dataframe of Heiken-Ashi bars with columns Open, High, Low, Close
    """
    # Validate Arguments
    open_ = df["Open"]
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    n = close.shape[0]
    ha = pd.DataFrame(
        {
            "Open": 0.5 * (open_.iloc[0] + close.iloc[0]),
            "High": high,
            "Low": low,
            "Close": 0.25 * (open_ + high + low + close),
        }
    )
    for i in range(1, n):
        ha["Open"].iloc[i] = 0.5 * (ha["Open"].iloc[i - 1] + ha["Close"].iloc[i - 1])
    ha["High"] = ha[["Open", "High", "Close"]].max(axis=1)
    ha["Low"] = ha[["Open", "Low", "Close"]].min(axis=1)
    return ha

class Candles:
    """Creates and maintains the raw candles of 1 minute dataframe.
    Also credate and maintains a grouped data from which is groups candles
    """
    def __init__(self, df: pd.DataFrame = None, group_sz: int = 5) -> None:
        self.group_sz = group_sz
        if df is None:
            self.df = None
            self.gf = None
        elif df.shape[0] < group_sz:
            self.df = df.copy()
            self.gf = None
        else:
            self.df = df.copy()
            self.gf = hybridDF(df=self.df, group_sz=self.group_sz)

    def addNewBar(self, bar: pd.DataFrame):
        """Appends the new bar (represent as single record dataframe) to orignal bars dataframe.
        Calculates a new hybrid bar and appends to the hybrid dataframe

        Args:
            bar (pd.DataFrame): The new bar. The format of this bar is a pd.DataFrame consiting of 
            a single record.
        """
        if self.df is  None:
            self.df = bar.copy()
        else:
            self.df = pd.concat([self.df, bar])
            N = self.df.shape[0]
            if N > self.group_sz:
                hfbar = ohlc(self.df.iloc[-self.group_sz :], bar_index_first=False)
                self.gf = pd.concat([self.gf, hfbar])
            elif N == self.group_sz:
                self.initHF()
            else:
                pass

    def getLatestGFgroup(self):
        """Extracts every group_sz candle starting from and including lastest bar
        """
        last_index = self.gf.shape[0] - 1
        gf = self.gf.iloc[range(last_index, 0, -self.group_sz)[::-1]]
        return gf