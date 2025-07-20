import json
import infra.db as db
from datetime import date
from domain.stock.controller.stock_controller import StockController

stockController = StockController()

if __name__ == "__main__":
    # 오늘 날짜
    today_date = date.today().strftime("%Y%m%d")
    today_date = "20250702"
    
    stockController.sync_kospi_listed_stocks(today_date)