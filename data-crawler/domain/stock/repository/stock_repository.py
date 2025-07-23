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
        
        #todo: 일단은 상폐종목 개수만큼 쿼리를 날리는걸로, 자주 발생하는 로직은 아니라 문제 없을 듯
        sql = '''
            UPDATE stocks
            SET is_delisted = 1
            WHERE ticker = %s
        '''
        for ticker in delisted_codes:
            cur.execute(sql, (ticker,))
        conn.commit()
    
    #종목 일별매매정보 insert 함수
    def insert_stock_daily_prices(self, daily_prices):
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            INSERT INTO daily_prices (
                ticker, trade_date, open_price, high_price, low_price,
                close_price, prev_change, change_rate, volume,
                amount, market_cap, listed_shares
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                open_price = VALUES(open_price),
                high_price = VALUES(high_price),
                low_price = VALUES(low_price),
                close_price = VALUES(close_price),
                prev_change = VALUES(prev_change),
                change_rate = VALUES(change_rate),
                volume = VALUES(volume),
                amount = VALUES(amount),
                market_cap = VALUES(market_cap),
                listed_shares = VALUES(listed_shares),
                updated_at = CURRENT_TIMESTAMP
        '''
        
        values = [
            (
                p['ISU_CD'],  # ticker
                p['BAS_DD'],      # trade_date
                p.get('TDD_OPNPRC'),
                p.get('TDD_HGPRC'),
                p.get('TDD_LWPRC'),
                p.get('TDD_CLSPRC'),
                p.get('CMPPREVDD_PRC'),
                p.get('FLUC_RT'),
                p.get('ACC_TRDVOL'),
                p.get('ACC_TRDVAL'),
                p.get('MKTCAP'),
                p.get('LIST_SHRS')
            ) for p in daily_prices
        ]
        
        cur.executemany(sql, values)
        conn.commit()
        
    
    
    # 종목 정보 조회시, 액면가(parval) 에 '무액면' 같은 문자열이 오는 경우 예외 처리를 위해 숫자 자료형인지 체크
    def _is_numeric(self, value) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False