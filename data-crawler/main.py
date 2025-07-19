import json
import infra.db as db
from fetch.listed_stocks import fetch_listed_stocks
from datetime import date

if __name__ == "__main__":
    
    # 오늘 날짜
    today_date = date.today().strftime("%Y%m%d")
    today_date = "20230702"
    
    # 상장 종목 리스트 조회
    stocks = fetch_listed_stocks(today_date)
    count = len(stocks["stock_list"])
    print(f"조회돈 종목 개수: {count} 개")
    
    # 기존 DB 에 있는 데이터와 비교해서 DB 정보 update
    conn = db.connect_db()
    existing_tickers = db.get_existing_tickers(conn)
    conn.close()
    
    # 종목 정보가 제대로 조회가 된 경우에만 db update
    if stocks is not None:
        conn = db.connect_db()
        db.update_stocks_info(conn, stocks["stock_list"])
        