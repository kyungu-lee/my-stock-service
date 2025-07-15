from config import get_db_config
import mariadb
from datetime import datetime as dt
from decimal import Decimal

db_config = get_db_config()

def connect_db():
    """
    Config 객체를 사용해 MariaDB에 연결하고 연결 정보를 출력합니다.
    연결 성공 시 연결 버전과 상태를 출력하고, Connection 객체를 반환합니다.
    """
    try:
        conn = mariadb.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()[0]
        
        print(f"✅ MariaDB 연결 성공! 버전: {version}")
        return conn
    except mariadb.Error as e:
        print(f"❌ MariaDB 연결 실패: {e}")
        raise
    
    
def update_stocks_info(conn, stock_list):
    sql = """
    INSERT INTO stocks (ticker, name, market, listing_date, par_value)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name         = VALUES(name),
        market       = VALUES(market),
        listing_date = VALUES(listing_date),
        par_value    = VALUES(par_value)
    """
    cur = conn.cursor()
    for stock in stock_list:
        # 액면가에 숫자가 아니라 문자열이 들어가는 경우가 있어서 Null 초기화좀 해주자
        if not isinstance(stock["PARVAL"],(int, float)):
            stock["PARVAL"] = None
            
        cur.execute(sql, (
            stock["ISU_SRT_CD"],          # ticker
            stock["ISU_NM"],              # name
            stock["MKT_TP_NM"],           # market
            dt.strptime(stock["LIST_DD"], "%Y%m%d").date(),
            stock["PARVAL"]
        ))
    conn.commit()
    
def get_existing_tickers(conn):
    sql = """
        SELECT ticker
        FROM stocks
    """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    tickers = [row[0] for row in rows]
    print(tickers)
    
    
    
    

        