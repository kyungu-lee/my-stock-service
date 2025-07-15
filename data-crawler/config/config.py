import os  # OS 환경변수 접근을 위한 모듈 임포트
from pathlib import Path  # 파일 경로 조작을 위한 Path 클래스 임포트
from dotenv import load_dotenv  # .env 파일을 읽어 환경변수를 설정하는 함수 임포트

# Load .env file from this directory
env_path = Path(__file__).parent / ".env"  # 이 config.py 파일이 있는 디렉토리의 .env 파일 경로 생성
load_dotenv(env_path)  # 위에서 지정한 .env 파일을 읽어 os.environ에 로드


# Database configuration object 반환
def get_db_config():
    """
    환경변수에서 읽어온 DB 연결 정보를 딕셔너리 형태로 반환합니다.
    """
    # Database configuration from environment
    DB_HOST = os.getenv("DB_HOST")  # 환경변수에서 DB 호스트 이름 조회
    DB_PORT = int(os.getenv("DB_PORT", "3306").strip('"'))  # 환경변수에서 DB 포트 조회, 기본값 3306, 문자열 따옴표 제거 후 정수 변환
    DB_USER = os.getenv("DB_USER")  # 환경변수에서 DB 사용자명 조회
    DB_PASS = os.getenv("DB_PASS")  # 환경변수에서 DB 비밀번호 조회
    DB_NAME = os.getenv("DB_NAME")  # 환경변수에서 사용할 데이터베이스 이름 조회

    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASS,
        "database": DB_NAME
    }


# API 요청 KEY
KRX_API_KEY = os.getenv("KRX_API_KEY")

# KRX API 요청 url
LISTED_STOCKS_URL = "http://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info"
