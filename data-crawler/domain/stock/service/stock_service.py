from domain.stock.api.fetch_kospi_stock_list import fetch_kospi_stock_list
from domain.stock.repository.stock_repository import StockRepository

class StockService:
    def __init__(self):
        self.stockRepository = StockRepository()

    def sync_kospi_stocks(self, base_date: str):
        data = fetch_kospi_stock_list(base_date)
        if not data or "stock_list" not in data:
            print("종목 데이터가 없습니다.")
            return
        
        fetched_stocks = data["stock_list"]
        fetched_codes = set(stock["ISU_SRT_CD"] for stock in fetched_stocks)
        existing_codes = set(self.stockRepository.get_all_stock_codes())
        
        # 신규 추가
        new_codes = fetched_codes - existing_codes
        new_stocks = [stock for stock in fetched_stocks if stock["ISU_SRT_CD"] in new_codes]
        self.stockRepository.insert_new_stocks(new_stocks);
        print(f"Inserted {len(new_stocks)} new stocks: {sorted(new_codes)}")
        
        # 상장 폐지 업데이트
        delisted_codes = existing_codes - fetched_codes
        self.stockRepository.update_is_delisted(delisted_codes)
        print(f"Marked {len(delisted_codes)} stocks as delisted: {sorted(delisted_codes)}")
        print()