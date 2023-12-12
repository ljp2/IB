import matplotlib.pyplot as plt
from matplotlib import axes

import numpy as np
import pandas as pd
import time
from multiprocessing import Process, Queue
import platform


class PlotProcess:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.q = Queue()
        plot_process = Process(target=self.plotProcess, args=(df, self.q))
        plot_process.daemon = True
        plot_process.start()

    def plotProcess(self, df: pd.DataFrame, q: Queue):
        x = 1
        print(f"Process Called {x}")
        while True:
            z = self.q.get()
            x += 1
            print(f"Process Queue {z} x = {x}")


def initialize(filename:str):
    df = pd.read_csv(filename, index_col=0, parse_dates=True)
    plot_process = PlotProcess(df)

    return plot_process


def waitforarrival():
    pass


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
    plot_process = initialize(filepath)
    # while not allstop:
    for i in range(3):
        waitforarrival()
        analyze()
        plot(plot_process)
        decide()
        summarize()
        
        time.sleep(1)



if __name__ == "__main__":
    main()


# # Enable interactive mode
# plt.ion()

# coldn = 'red'
# colup = 'green'
# width = (df.index[1] - df.index[0]) * 0.6
# width2 = width * 0.3

# def plotBar(ax:axes, df:pd.DataFrame, i:int):
#     up = df.iloc[i:i+1]
#     ax.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=colup)

# def decide():
#     input()

# # Create a figure and axis
# fig, ax = plt.subplots()
# ax.set_xlim(df.index[0], df.index[-1])
# ax.set_ylim(df.Low.min(), df.High.max())

# for i in range(10):
#     plotBar(ax, df, i)
#     plt.pause(.1)
#     decide()


# time.sleep(5)

# Plot the initial data
# line, = ax.plot(x, y, label='Sin(x)')

# # Set labels and title
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_title('Interactive Matplotlib Example')

# # Show legend
# ax.legend()

# Display the plot
# plt.show()

# # Now, you can interactively update the plot, for example, by modifying the data
# for i in range(100):
#     y = np.sin(x + i * 0.1)
#     line.set_ydata(y)

#     # Pause to allow the plot to update
#     plt.pause(0.1)

# # Turn off interactive mode when done
# plt.ioff()

# # Display the final plot (optional)
# plt.show()
