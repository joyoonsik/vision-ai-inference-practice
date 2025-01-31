import sqlite3
import uuid
from datetime import datetime, timedelta
# 데이터베이스 연결 (파일로 저장되며, 파일 이름은 예시로 'example.db')
conn = sqlite3.connect('pico.db')
cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS 피코 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT,
    uuid TEXT UNIQUE,
    is_defective INTEGER,
    defect_reason TEXT,
    image_url TEXT
)
'''
cursor.execute(create_table_query)
# 데이터 삽입 함수
def insert_data(datetime_value, uuid_value, is_defective, image_url, defect_reason=None):
    insert_query = '''
    INSERT INTO 피코 (datetime, uuid, is_defective, image_url, defect_reason)
    VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (datetime_value, uuid_value, is_defective, image_url, defect_reason))
    conn.commit()
    # 데이터 예제
datetime_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 날짜와 시간
uuid_value = str(uuid.uuid4())  # UUID 생성
is_defective = 0  # 불량품인 경우 (1: 불량, 0: 양품)
image_url = "box_image_20250131_145824.jpg"
defect_reason = "None"  # 불량 사유 (양품인 경우 None 또는 생략 가능)
# 데이터 삽입 호출
insert_data(datetime_value, uuid_value, is_defective, image_url, defect_reason)
# # # 최근 12시간 데이터 조회 쿼리
query = '''
SELECT * FROM 피코
'''
# # # 현재 시간과 12시간 전 시간 계산
now = datetime.now()
twelve_hours_ago = now - timedelta(hours=12)
# 12시간 전 시간을 문자열로 변환 (ISO 형식)
twelve_hours_ago_str = twelve_hours_ago.strftime("%Y-%m-%d %H:%M:%S")
# # # 데이터 조회 실행
cursor.execute(query)
results = cursor.fetchall()
# # 결과 출력
for row in results:
    print(row)
print("hi")
# # 연결 종료
conn.close()
