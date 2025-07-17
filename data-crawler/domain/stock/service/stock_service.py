from domain.stock.api.fetch_kospi_stock_list import fetch_kospi_stock_list
from domain.stock.repository.stock_repository import StockRepository

class StockService:
    def __init__(self):
        self.repository = StockRepository()

    def sync_kospi_stocks(self, base_date: str):
        data = fetch_kospi_stock_list(base_date)
        if not data or "stock_list" not in data:
            print("종목 데이터가 없습니다.")
            return
        
        fetched_stocks = data["stock_list"]
        fetched_codes = set(stock["code"] for stock in fetched_stocks)
        existing_codes = set(self.repository.get_all_stock_codes())
        
        


