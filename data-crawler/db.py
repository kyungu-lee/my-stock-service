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
    
    
def update_stocks(conn, stock_list):
    """
    stocks 테이블에 들어온 종목 리스트를
    - 없으면 INSERT
    - 있으면 name/market/listing_date/par_value를 UPDATE
    처리합니다.
    """
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
        # 액면가에 숫자가 아니라 문자열이 들어가는 경우가 있네
        parval = stock["PARVAL"]
        if parval == '무액면':
            parval = None
        
        cur.execute(sql, (
            stock["ISU_SRT_CD"],          # ticker
            stock["ISU_NM"],              # name
            stock["MKT_TP_NM"],           # market
            dt.strptime(stock["LIST_DD"], "%Y%m%d").date(),
            parval
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
    
    
    
    

        
# 번호	항목명	출력명	Data Type
# 1	표준코드	ISU_CD	string()
# 2	단축코드	ISU_SRT_CD	string()
# 3	한글 종목명	ISU_NM	string()
# 4	한글 종목약명	ISU_ABBRV	string()
# 5	영문 종목명	ISU_ENG_NM	string()
# 6	상장일	LIST_DD	string()
# 7	시장구분	MKT_TP_NM	string()
# 8	증권구분	SECUGRP_NM	string()
# 9	소속부	SECT_TP_NM	string()
# 10	주식종류	KIND_STKCERT_TP_NM	string()
# 11	액면가	PARVAL	string()
# 12	상장주식수	LIST_SHRS	string()
        