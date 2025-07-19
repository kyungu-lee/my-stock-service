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
        fetched_codes = set(stock["ISU_SRT_CD"] for stock in fetched_stocks)
        existing_codes = set(self.repository.get_all_stock_codes())
        
        #todo: db 에 신규로 insert 해야함    
        new_codes = fetched_codes - existing_codes
        new_stocks = [stock for stock in fetched_stocks if stock["ISU_SRT_CD"] in new_codes]
        StockRepository.insert_new_stocks(new_stocks);
        
        
        #todo: db 에 상장폐지 컬럼 업데이트 해야함
        delisted_codes = existing_codes - fetched_codes
        delisted_stocks = [stock for stock in fetched_stocks if stock["ISU_SRT_CD"] in delisted_codes]
        
    
    
    
        


