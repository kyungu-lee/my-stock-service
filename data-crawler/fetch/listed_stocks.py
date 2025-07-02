from config import LISTED_STOCKS_URL
from config import KRX_API_KEY
import requests


def fetch_listed_stocks(base_date):
    """
    GET 요청으로 상장 종목 리스트를 조회하고, JSON 결과를 출력 및 반환합니다.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    data = {
        "apiid": "stk_isu_base_info",
        "authKey": KRX_API_KEY,
        "reqType": "json",
        "baseDate": base_date
    }
    try:
        # POST 요청 수행
        response = requests.post(LISTED_STOCKS_URL, data=data, headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        data = response.json()      # JSON 파싱
        print(data)                 # 결과 JSON 출력
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ 상장 종목 조회 실패: {e}")
        return None


if __name__ == "__main__":
    # 예시: apiid="123", auth_key="ABCDEF", req_type="01", base_date="20250701"
    fetch_listed_stocks("123", "ABCDEF", "01", "20250701")
