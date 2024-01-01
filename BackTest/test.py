import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QKeyEvent, QMouseEvent

import pyqtgraph as pg


candles_to_draw = [
    (1, 4, 5, 3, 3.5),
    (2, 3.5, 4, 2.5, 3),
    (3, 3, 3.5, 2, 2),
    (4, 2, 2.5, 1.5, 2.5),
]
current_candle_index = 0



class CandlestickWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super(CandlestickWidget, self).__init__(parent)
        
        self.crosshair_vline = pg.InfiniteLine(angle=90, movable=False, pen='w')
        self.crosshair_hline = pg.InfiniteLine(angle=0, movable=False, pen='w')
        self.addItem(self.crosshair_vline, ignoreBounds=True)
        self.addItem(self.crosshair_hline, ignoreBounds=True)

        self.coordinate_label = pg.TextItem("", anchor=(0, 1), color=(255, 255, 255))
        self.addItem(self.coordinate_label, ignoreBounds=True)
        
        self.is_left_button_pressed = False
        self.data = []
        
    def setAxisLimits(self, xmin, xmax, ymin, ymax):
        self.setRange(xRange=(xmin, xmax), yRange=(ymin, ymax))

    def plotCandle(self, candle_data):
        time, open_price, high, low, close_price = candle_data

        # Candle body
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

        self.data.append(candle_data)

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            pos = ev.pos()
            if self.sceneBoundingRect().contains(QPointF(pos)):
                mouse_point = self.getViewBox().mapSceneToView(QPointF(pos))
                self.crosshair_vline.setValue(mouse_point.x())
                self.crosshair_hline.setValue(mouse_point.y())
                self.is_left_button_pressed = True

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.is_left_button_pressed = False

    def mouseMoveEvent(self, ev: QMouseEvent):
        pos = ev.pos()
        if self.sceneBoundingRect().contains(QPointF(pos)):
            mouse_point = self.getViewBox().mapSceneToView(QPointF(pos))
            self.crosshair_vline.setValue(mouse_point.x())
            self.crosshair_hline.setValue(mouse_point.y())
            self.updateCoordinateLabel(mouse_point)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Space:
            self.drawNextCandle()

    def updateCoordinateLabel(self, mouse_point):
        x, y = mouse_point.x(), mouse_point.y()
        self.coordinate_label.setPos(x, y)
        self.coordinate_label.setText(f"({x:.2f}, {y:.2f})")

    def drawNextCandle(self):
        global candles_to_draw, current_candle_index
        if current_candle_index < len(candles_to_draw):
            candle_data = candles_to_draw[current_candle_index]
            self.plotCandle(candle_data)
            current_candle_index += 1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

            
            
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.candlestickWidget = CandlestickWidget(self)
        
        self.candlestickWidget.setRange(xRange=(0,5), yRange=(0,5))
        
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
            self.candlestickWidget.plotCandle(candle_data)
            current_candle_index += 1

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
