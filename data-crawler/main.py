import json
import db
from fetch.listed_stocks import fetch_listed_stocks

if __name__ == "__main__":
    # 상장 종목 리스트 조회
    base_date = "20250702"
    stocks = fetch_listed_stocks(base_date)
    # if stocks is not None:
        # filename = f"stocks_{base_date}.json"
        # with open(filename, "w", encoding="utf-8") as f:
        #     json.dump(stocks, f, ensure_ascii=False, indent=2)
        # print(f"Saved JSON data to {filename}")