from domain.stock.api.fetch_kospi_stock_list import fetch_kospi_stock_list
from domain.stock.repository.stock_repository import StockRepository

class StockService:
    def __init__(self):
        self.repository = StockRepository()

    def sync_kospi_stocks(self, base_date: str):
        data = fetch_kospi_stock_list(base_date)
        if not data or "stock_list" not in data:
            print("⚠️ 유효한 종목 데이터가 없습니다.")
            return
        # todo : 디비에 있는 데이터 확인하고, 추가로 insert 하거나 상장폐지 여부 update 해야함
        for stock in data["stock_list"]:
            self.repository.upsert_stock(stock)