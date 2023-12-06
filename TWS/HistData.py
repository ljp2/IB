import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import threading
import time
from datetime import datetime

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.event_done = threading.Event()
        self.bars = []

    def historicalData(self, reqId, bar:BarData):
        self.bars.append( {'Date': bar.date.rsplit(' ', 1)[0], 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close, 'Volume': bar.volume} )

        
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.event_done.set()
        
        
def websocket_con():
    app.run()    


def getBarsOneDayOneMinute(end_date:str, contract_month:str):
    global app
    app.event_done.clear()

    contract = Contract()
    contract.symbol = "ES"
    contract.secType = "FUT"
    contract.exchange = "CME"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = contract_month

    # endDateTime=''
    endDateTime=f'{end_date}-23:59:59'
    # endDateTime='20231130-23:59:59'
    print('endDateTime', endDateTime)

    app.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime=endDateTime,
        durationStr="1 D",
        barSizeSetting="30 mins",
        whatToShow="TRADES",
        useRTH=1,
        formatDate=1,
        keepUpToDate=0,
        chartOptions = []
    )

    app.event_done.wait()
    df:pd.DataFrame = pd.DataFrame(app.bars)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    return df;



def main():
    global app
    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    con_thread = threading.Thread(target=websocket_con, daemon=True)
    con_thread.start()
    time.sleep(1)



    df = getBarsOneDayOneMinute(end_date='20231130', contract_month='202403')
    print(df)


    app.disconnect()
    print("MAIN DONE")


main()

import datetime

def printday(d:datetime.datetime):
    if d.weekday() <= 4:
        print(d, '\t', d.date(), '\t', d.day, '\t', d.weekday())


d = datetime.datetime.now()
dt = datetime.timedelta(days=1)

printday(d)
for i in range(20):
    d = d - dt
    printday(d)