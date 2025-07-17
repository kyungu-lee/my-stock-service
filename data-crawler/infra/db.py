from config.config import get_db_config
import mariadb
from datetime import datetime as dt
from decimal import Decimal

db_config = get_db_config()

def connect_db():
    try:
        conn = mariadb.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()[0]
        
        print(f"MariaDB 연결 성공! 버전: {version}")
        return conn
    except mariadb.Error as e:
        print(f"MariaDB 연결 실패: {e}")
        raise
    