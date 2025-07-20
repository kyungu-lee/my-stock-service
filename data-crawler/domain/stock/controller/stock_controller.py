from domain.stock.service.stock_service import StockService

class StockController:
    def __init__(self):
        self.stockService = StockService()

    # KOSPI 종목 정보 가져와서 DB 정보 최신화
    def sync_kospi_listed_stocks(self, base_date: str):
        self.stockService.sync_kospi_stocks(base_date)