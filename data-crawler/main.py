import json
import db
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
    
    
    # 종목 정보가 제대로 조회가 된 경우만 파일로 생성
    if stocks is not None:
        filename = f"stocks_{today_date}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stocks, f, ensure_ascii=False, indent=2)
        print(f"종목 정보 파일 저장완료! {filename}")
        
    # DB 정보 업데이트
        
        
        
#     번호	항목명	출력명	Data Type
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
        
        
