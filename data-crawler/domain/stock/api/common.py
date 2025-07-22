# 데이터 검증
def check_data_exists(data):
    # 데이터에 "OutBlock_1" 키가 존재하고 값이 비어있지 않은지 확인
    return "OutBlock_1" in data and data["OutBlock_1"]

