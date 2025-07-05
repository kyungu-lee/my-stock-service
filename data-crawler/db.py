from config import get_db_config
import mariadb

db_config = get_db_config()

def connect_db():
    """
    Config 객체를 사용해 MariaDB에 연결하고 연결 정보를 출력합니다.
    연결 성공 시 연결 버전과 상태를 출력하고, Connection 객체를 반환합니다.
    """
    try:
        conn = mariadb.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()[0]
        
        print(f"✅ MariaDB 연결 성공! 버전: {version}")
        return conn
    except mariadb.Error as e:
        print(f"❌ MariaDB 연결 실패: {e}")
        raise
