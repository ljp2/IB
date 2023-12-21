
import time

import arrivals
import plots

import initialize

if __name__ == "__main__":
    barfilename = '20231130'
    df = initialize.initialize(barfilename)
    plot = plots.Plot(df, barfilename)
    quotes = arrivals.Arrivals(df)
    
    # for i in range(5):
    #     time.sleep(1)
    #     print(next(quotes))
    input('hey')