import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
import threading
import time
import datetime


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.event_done = threading.Event()
        self.bars = None

    def historicalData(self, reqId, bar: BarData):
        self.bars.append(
            {
                "Date": bar.date.rsplit(" ", 1)[0],
                "Open": bar.open,
                "High": bar.high,
                "Low": bar.low,
                "Close": bar.close,
                "Volume": bar.volume,
            }
        )

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.event_done.set()


def websocket_con():
    app.run()


def getBarsOneDayOneMinute(end_date: str):
    global app
    app.event_done.clear()
    app.bars = []

    contract = Contract()

    contract = Contract()
    contract.symbol = "SPX"
    contract.secType = "IND"
    contract.exchange = "CBOE"
    contract.currency = "USD"

    endDateTime = f"{end_date} 23:59:59 America/New_York"

    app.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime=endDateTime,
        durationStr="1 D",
        barSizeSetting="1 min",
        whatToShow="TRADES",
        useRTH=1,
        formatDate=1,
        keepUpToDate=0,
        chartOptions=[],
    )

    app.event_done.wait()
    df: pd.DataFrame = pd.DataFrame(app.bars)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    return df


def main(desired_number_days: int, directory: str = ""):
    global app
    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    con_thread = threading.Thread(target=websocket_con, daemon=True)
    con_thread.start()
    time.sleep(1)

    dt = datetime.timedelta(days=1)
    day = datetime.datetime.now()

    number_gotdays = 0
    while number_gotdays < desired_number_days:
        end_date = day.strftime("%Y%m%d")
        df = getBarsOneDayOneMinute(end_date=end_date)

        index0: pd.Timestamp = df.index[0]
        gotdate = df.index[0].strftime('%Y%m%d')
        gotweekday = index0.day_name()
        number_gotdays += 1
        print(gotdate, '\t', gotweekday, '\t', df.shape)

        filename = f'{directory}/{gotdate}.csv'
        df.to_csv(filename)

        day = index0 - dt

    app.disconnect()
    print("MAIN DONE")


main(desired_number_days=7, directory='~/junk')
