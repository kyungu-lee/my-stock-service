import json
import infra.db as db
from datetime import date
from domain.stock.controller.stock_controller import StockController

stockController = StockController()

if __name__ == "__main__":
    # 오늘 날짜
    today_date = date.today().strftime("%Y%m%d")
    today_date = "20250702"
    
    # 종목정보 조회를 통해서 거래일인지 확인한 후에 KRX 데이터를 수집한다
    if stockController.sync_kospi_listed_stocks(today_date):
        stockController.sync_kospi_daily_prices(today_date)
    else:
        print(f"{today_date}는 거래일이 아닙니다.")