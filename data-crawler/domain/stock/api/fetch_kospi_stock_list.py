from config.config import LISTED_STOCKS_API_URL
from config.config import KRX_API_KEY
from .common import check_data_exists

import requests

def fetch_kospi_stock_list(base_date):
    headers = {
        "AUTH_KEY": KRX_API_KEY,
    }
    params = {
        "basDd": base_date,
    }
    try:
        # GET 요청
        response = requests.get(LISTED_STOCKS_API_URL, params=params ,headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        data = response.json()      # JSON 파싱
        
        # json 데이터가 넘어온 경우만 전달
        if check_data_exists(data):
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f" 상장 종목 조회 로직 실행 중 예외 발생: {e}")
        return None
    
'''
번호	항목명	출력명	Data Type
1	표준코드	ISU_CD	string()
2	단축코드	ISU_SRT_CD	string()
3	한글 종목명	ISU_NM	string()
4	한글 종목약명	ISU_ABBRV	string()
5	영문 종목명	ISU_ENG_NM	string()
6	상장일	LIST_DD	string()
7	시장구분	MKT_TP_NM	string()
8	증권구분	SECUGRP_NM	string()
9	소속부	SECT_TP_NM	string()
10	주식종류	KIND_STKCERT_TP_NM	string()
11	액면가	PARVAL	string()
12	상장주식수	LIST_SHRS	string()
'''