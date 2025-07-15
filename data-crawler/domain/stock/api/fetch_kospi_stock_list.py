from config.config import LISTED_STOCKS_URL
from config.config import KRX_API_KEY
import requests

def fetch_listed_stocks(base_date):
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
        if "OutBlock_1" in data and data["OutBlock_1"]:
            data["stock_list"] = data.pop("OutBlock_1")
            print(f"✅ 상장 종목 조회 성공!")
            return data
        else:
            print(f"❌ 거래일이 아닙니다.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 상장 종목 조회 실패: {e}")
        return None