from infra.db import connect_db

class StockRepository:
    def get_all_stock_codes(self):
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            SELECT ticker
            FROM stocks
            WHERE market = 'KOSPI'
        '''
        cur.execute(sql)
        results = cur.fetchall()
        codes = [row[0] for row in results]
        return codes

    def insert_new_stocks(self, stock_list: list[dict]):
        if not stock_list:
            return
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            INSERT INTO stocks (ticker, name, market, listing_date, par_value, is_delisted)
            VALUES (%s, %s, %s, %s, %s, 0)
        '''
        for stock in stock_list:
            cur.execute(sql, (
                stock["code"],
                stock["name"],
                stock["market"],
                stock.get("listing_date", None),
                stock.get("par_value", 0.0)
            ))
        conn.commit()