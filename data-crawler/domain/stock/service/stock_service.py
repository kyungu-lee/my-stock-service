from domain.stock import api
from domain.stock.repository.stock_repository import StockRepository

class StockService:
    def __init__(self):
        self.stockRepository = StockRepository()

    # 상장 종목 정보 API 조회 및 DB 업데이트
    def sync_kospi_stocks(self, base_date: str):
        # KRX 에 API 요청
        response = api.fetch_kospi_stock_list(base_date)
        data = response.get("OutBlock_1",[])
        if not data:
            print("종목 데이터가 없습니다.")
            return None
        
        fetched_stocks = data
        fetched_codes = set(stock["ISU_SRT_CD"] for stock in fetched_stocks)
        existing_codes = set(self.stockRepository.get_all_stock_codes())
        print(fetched_codes)
        print(existing_codes)
        
        # 신규 추가
        new_codes = fetched_codes - existing_codes
        new_stocks = [stock for stock in fetched_stocks if stock["ISU_SRT_CD"] in new_codes]
        self.stockRepository.insert_new_stocks(new_stocks);
        print(f"Inserted {len(new_stocks)} new stocks: {sorted(new_codes)}")
        
        # 상장 폐지 업데이트
        delisted_codes = existing_codes - fetched_codes
        self.stockRepository.update_is_delisted(delisted_codes)
        print(f"Marked {len(delisted_codes)} stocks as delisted: {sorted(delisted_codes)}")
        return data
        
    # 일별 시세 API 조회 및 DB 업데이트
    def sync_kospi_daily_prices(self, base_date: str):
        response = api.fetch_kospi_stock_daily_prices(base_date);
        data = response.get("OutBlock_1",[])
        if not data:
            print("일별 매매정보가 없습니다.")
            return None
        self.stockRepository.insert_stock_daily_prices(data)
        
        