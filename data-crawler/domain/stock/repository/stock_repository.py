from infra.db import connect_db

class StockRepository:
    def get_all_stock_codes(self):
        conn = connect_db()
        cur = conn.cursor()
        sql = '''
            SELECT code
            FROM stocks
            WHERE market = 'KOSPI'
        '''
        cur.execute(sql)
        results = cur.fetchall()
        codes = [row[0] for row in results]
        return codes

