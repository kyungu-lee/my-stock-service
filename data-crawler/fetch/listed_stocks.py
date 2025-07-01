from ..config import LISTED_STOCKS_URL
import requests


def fetch_listed_stocks(params=None):
    """
    GET 요청으로 상장 종목 리스트를 조회하고, JSON 결과를 출력 및 반환합니다.
    """
    # GET 요청 수행
    response = requests.get(LISTED_STOCKS_URL, params=params)
    response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
    data = response.json()      # JSON 파싱
    print(data)                 # 결과 JSON 출력
    return data

if __name__ == "__main__":
    # 직접 실행 시 기본 파라미터(None)로 조회
    fetch_listed_stocks()

