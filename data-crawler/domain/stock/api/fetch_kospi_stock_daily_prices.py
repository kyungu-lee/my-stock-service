from config.config import KOSPI_DAILY_PRICE_API_URL
from config.config import KRX_API_KEY
import requests
from .common import check_data_exists

def fetch_kospi_stock_daily_prices(base_date):
    headers = {
        "AUTH_KEY": KRX_API_KEY,
    }
    params = {
        "basDd": base_date,
    }
    try:
        # GET 요청
        response = requests.get(KOSPI_DAILY_PRICE_API_URL, params=params ,headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        data = response.json()      # JSON 파싱
        
        # json 데이터가 넘어온 경우만 전달
        if check_data_exists(data):
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f" 일별 매매정보 API 요청중 에러 발생: {e}")
        return None

    
''' 종목별로 하기 데이터가 모두 넘어옴
번호	항목명	출력명	Data Type
1	기준일자	BAS_DD	string()
2	종목코드	ISU_CD	string()
3	종목명	ISU_NM	string()
4	시장구분	MKT_NM	string()
5	소속부	SECT_TP_NM	string()
6	종가	TDD_CLSPRC	string()
7	대비	CMPPREVDD_PRC	string()
8	등락률	FLUC_RT	string()
9	시가	TDD_OPNPRC	string()
10	고가	TDD_HGPRC	string()
11	저가	TDD_LWPRC	string()
12	거래량	ACC_TRDVOL	string()
13	거래대금	ACC_TRDVAL	string()
14	시가총액	MKTCAP	string()
15	상장주식수	LIST_SHRS	string()
'''
