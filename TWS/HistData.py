import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import threading
import time

class TradingApp(EWrapper, EClient):
    def __init__(self, event_Done:threading.Event):
        EClient.__init__(self, self)
        self.event_done = event_Done
        self.bars = []

    def historicalData(self, reqId, bar):
        self.bars.append( {'Date': bar.date, 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close, 'Volume': bar.volume} )

        
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.event_done.set()
        
        
def websocket_con():
    app.run()    

event_done:threading.Event = threading.Event()
app = TradingApp(event_done)
app.connect("127.0.0.1", 7497, clientId=1)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)

contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202403"

app.reqHistoricalData(
    reqId=1,
    contract=contract,
    endDateTime="",
    durationStr="1 D",
    barSizeSetting="30 mins",
    whatToShow="TRADES",
    useRTH=1,
    formatDate=1,
    keepUpToDate=0,
    chartOptions = []
)

event_done.wait()
df:pd.DataFrame = pd.DataFrame(app.bars)
print(df)


app.disconnect()
print("MAIN DONE")
