import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, \
                            QPushButton
import pyqtgraph as pg
import numpy as np

candles_to_draw = [
    (1, 4, 5, 3, 3.5),
    (2, 3.5, 4, 2.5, 3),
    (3, 3, 3.5, 2, 2),
    (4, 2, 2.5, 1.5, 2.5),
]
current_candle_index = 0  


class OHLCplot(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.setBackground('w')
        
        self.p1 = self.addPlot(0,0)
        self.p1.setRange(xRange=(0,5), yRange=(0,5))
        self.p1.showGrid(x=True, y=True)
        
        # self.p2 = self.addPlot(1,0)
        # self.p2.setRange(xRange=(0,5), yRange=(0,5))
        # self.p2.showGrid(x=True, y=True)
        
        self.candle_width = 0.3
        self.wick_width = 0.03
        
         
    def plot_candle(self, time, open_price, high, low, close_price):
        if open_price < close_price:
            # Bullish candle
            self.p1.addItem(pg.BarGraphItem(x=[time], height=[close_price - open_price], width=self.candle_width, y=open_price, brush='g'))
            self.p1.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='g'))
        elif open_price > close_price:
            # Bearish candle
            self.p1.addItem(pg.BarGraphItem(x=[time], height=[open_price - close_price], width=self.candle_width, y=close_price, brush='r'))
            self.p1.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='r'))
        else:
            # Open price equals close price (neutral candle)
            self.p1.addItem(pg.BarGraphItem(x=[time], height=[0.1], width=self.candle_width, y=open_price, brush='b'))
            self.p1.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='b'))     

    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.candlestickWidget = OHLCplot()
        
        # # self.candlestickWidget.setRange(xRange=(0,5), yRange=(0,5))
        # self.candlestickWidget.setAxisLimits(0,5,0,5)
        
        # self.setCentralWidget(self.candlestickWidget)

        self.drawButton = QPushButton('Draw Candle', self)
        self.drawButton.clicked.connect(self.drawNextCandle)

        layout = QVBoxLayout()
        layout.addWidget(self.candlestickWidget)
        layout.addWidget(self.drawButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        for i in range(len(candles_to_draw)):
            time, open_price, high, low, close_price = candles_to_draw[i]
            print(time, open_price, high, low, close_price)
            self.candlestickWidget.plot_candle(time, open_price, high, low, close_price)

    def drawNextCandle(self):
        global candles_to_draw, current_candle_index
        if current_candle_index < len(candles_to_draw):
            candle_data = candles_to_draw[current_candle_index]
            time, open_price, high, low, close_price = candle_data
            self.candlestickWidget.plot_candle(time, open_price, high, low, close_price)
            current_candle_index += 1


    
def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())   
    

if __name__ == '__main__':
    main()
