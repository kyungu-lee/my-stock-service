from domain.stock.service.stock_service import StockService

class StockController:
    def __init__(self):
        self.stockService = StockService()

    def sync_kospi_listed_stocks(self, base_date: str):
        """KRX에서 KOSPI 종목 정보를 가져와서 DB와 비교 후 업데이트"""
        self.stockService.sync_kospi_stocks(base_date)