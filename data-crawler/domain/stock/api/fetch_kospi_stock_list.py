from config.config import LISTED_STOCKS_URL
from config.config import KRX_API_KEY
import requests

def fetch_kospi_stock_list(base_date):
    """
    GET 요청으로 상장 종목 리스트를 조회하고, JSON 결과를 출력 및 반환합니다.
    """
    headers = {
        "AUTH_KEY": KRX_API_KEY,
    }
    params = {
        "basDd": base_date,
    }
    try:
        # GET 요청
        response = requests.get(LISTED_STOCKS_URL, params=params ,headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        data = response.json()      # JSON 파싱
        
        # json 데이터가 넘어온 경우만 전달
        if validate_data(data):
            data = transform_to_stock_list(data)
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f" 상장 종목 조회 로직 실행 중 예외 발생: {e}")
        return None
    
# 데이터 검증
def validate_data(data):
    # 데이터에 "OutBlock_1" 키가 존재하고 값이 비어있지 않은지 확인
    return "OutBlock_1" in data and data["OutBlock_1"]

# json 데이터 key 이름 변경
def transform_to_stock_list(data):
    # "OutBlock_1" 키를 "stock_list"로 변경
    data["stock_list"] = data.pop("OutBlock_1")
    return data
