import pandas as pd 

def ohlc(df:pd.DataFrame):
    x = [{
        'Open' : df.Open.iloc[0],
        'High' : df.High.max(),
        'Low' : df.Low.min(),
        'Close' : df.Close.iloc[-1]
    }]
    zf =  pd.DataFrame(x, index=[df.index[0]])
    return zf

df = pd.read_csv('c:/Data/20231130.csv', index_col=0, parse_dates=True)

print(df.head(7))

inc = 3

s = df.shape[0]
ngroups= s // inc
N = ngroups * inc
first = s - N

xf = pd.DataFrame()
start = first
last = start + inc
while start < s:
    wf = ohlc(df.iloc[start:last])
    xf = pd.concat([xf, wf])  #, ignore_index=True)
    start += inc
    last += inc

print(xf.head(ngroups))
