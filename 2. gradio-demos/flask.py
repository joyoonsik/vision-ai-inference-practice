from flask import Flask, render_template, jsonify, request
import sqlite3
import os
app = Flask(__name__)
# SQLite DB에서 데이터 가져오기
def get_data_from_db(defective=None):
    # 데이터베이스 경로 설정 (프로젝트 구조에 따라 조정 필요)
    db_path = os.path.join(os.path.dirname(__file__), 'pico.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 기본 쿼리
    query = "SELECT * FROM 피코"
    params = []
    # 필터링 조건 추가
    if defective is not None:
        query += " WHERE is_defective = ?"
        params.append(defective)
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    # 결과 반환
    return data
@app.route('/')
def index():
    return render_template('test.html')
@app.route('/get_data')
def get_data():
    # 요청 파라미터에서 'defective' 값을 가져옵니다 (0, 1 또는 없음)
    defective = request.args.get('defective')
    if defective is not None:
        try:
            defective = int(defective)
            if defective not in (0, 1):
                defective = None
        except ValueError:
            defective = None
    data = get_data_from_db(defective)
    # 데이터베이스 컬럼 순서에 따라 JSON 형태로 변환 (필요 시 키 추가 가능)
    data_dict = [
        {
            "id": row[0],
            "datetime": row[1],
            "uuid": row[2],
            "is_defective": row[3],
            "defect_reason": row[4],
            "image_url": row[5]
        }
        for row in data
    ]
    return jsonify(data_dict)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
