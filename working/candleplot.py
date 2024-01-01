import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, \
                            QPushButton
import pyqtgraph as pg
import numpy as np

class CandlestickWidget(pg.PlotWidget):
    def __init__(self):
        super(CandlestickWidget, self).__init__()

        # Create an OHLC plot
        self.setBackground("w")
        self.showGrid(x=True, y=True)
        
    def setAxisLimits(self, xmin, xmax, ymin, ymax):
        self.setRange(xRange=(xmin, xmax), yRange=(ymin, ymax))
         
    def plot_candle(self, time, open_price, high, low, close_price):
        if open_price < close_price:
            # Bullish candle
            self.addItem(pg.BarGraphItem(x=[time], height=[close_price - open_price], width=0.2, y=open_price, brush='g'))
            self.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='g'))
        elif open_price > close_price:
            # Bearish candle
            self.addItem(pg.BarGraphItem(x=[time], height=[open_price - close_price], width=0.2, y=close_price, brush='r'))
            self.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='r'))
        else:
            # Open price equals close price (neutral candle)
            self.addItem(pg.BarGraphItem(x=[time], height=[0.1], width=0.2, y=open_price, brush='b'))
            self.addItem(pg.PlotDataItem(x=[time, time], y=[low, high], pen='b'))     

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.candlestickWidget = CandlestickWidget()
        
        # self.candlestickWidget.setRange(xRange=(0,5), yRange=(0,5))
        self.candlestickWidget.setAxisLimits(0,5,0,5)
        
        self.setCentralWidget(self.candlestickWidget)

        self.drawButton = QPushButton('Draw Candle', self)
        self.drawButton.clicked.connect(self.drawNextCandle)

        layout = QVBoxLayout()
        layout.addWidget(self.candlestickWidget)
        layout.addWidget(self.drawButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def drawNextCandle(self):
        global candles_to_draw, current_candle_index
        if current_candle_index < len(candles_to_draw):
            candle_data = candles_to_draw[current_candle_index]
            time, open_price, high, low, close_price = candle_data
            self.candlestickWidget.plot_candle(time, open_price, high, low, close_price)
            current_candle_index += 1

candles_to_draw = [
    (1, 4, 5, 3, 3.5),
    (2, 3.5, 4, 2.5, 3),
    (3, 3, 3.5, 2, 2),
    (4, 2, 2.5, 1.5, 2.5),
]
current_candle_index = 0  
    
def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.show()
    sys.exit(app.exec())   
    

if __name__ == '__main__':
    main()
