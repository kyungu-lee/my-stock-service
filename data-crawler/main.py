import db
from fetch.listed_stocks import fetch_listed_stocks

if __name__ == "__main__":
    # 상장 종목 리스트 조회
    stocks = fetch_listed_stocks("20250702")
    print("Fetched stocks:", stocks)