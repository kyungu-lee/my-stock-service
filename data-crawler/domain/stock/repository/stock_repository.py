from infra.db import connect_db

class StockRepository:
    # 현재 상장된 전체 종목 조회 함수
    def get_all_stock_codes(self):
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            SELECT ticker
            FROM stocks
            WHERE market = 'KOSPI'
                AND is_delisted = 0
        '''
        cur.execute(sql)
        results = cur.fetchall()
        codes = [row[0] for row in results]
        return codes

    # 신규 상장 또는 전체 상장 종목 DB INSERT 함수
    def insert_new_stocks(self, new_stocks: list[dict]):
        if not new_stocks:
            return
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            INSERT INTO stocks (ticker, name, market, listing_date, par_value, is_delisted)
            VALUES (%s, %s, %s, %s, %s, 0)
        '''
        for stock in new_stocks:
            if not self._is_numeric(stock['PARVAL']):
                stock['PARVAL'] = 0
                
            cur.execute(sql, (
                stock["ISU_SRT_CD"],
                stock["ISU_NM"],
                stock["MKT_TP_NM"],
                stock.get("LIST_DD", None),
                stock.get("PARVAL")
            ))
        conn.commit()
        
    # 상장폐지 컬럼 업데이트 함수, 1: 상폐, 0: 상장
    def update_is_delisted(self, delisted_codes: set[str]):
        if not delisted_codes:
            return
        conn = connect_db()
        cur = conn.cursor()
        
        #개선점: 일단은 상폐종목 개수만큼 쿼리를 날리는걸로, 자주 발생하는 로직은 아니라 문제 없을 듯
        sql = '''
            UPDATE stocks
            SET is_delisted = 1
            WHERE ticker = %s
        '''
        for ticker in delisted_codes:
            cur.execute(sql, (ticker,))
        conn.commit()
        
    
    def _is_numeric(self, value) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False