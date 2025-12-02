from flask import Flask, request, jsonify # Flask = 서버 만드는 도구, request = 프론트에서 보낸
from flask_cors import CORS # CORS = 프론트에서 서버로 요청할 때 허용해주는 기능
import sqlite3

app = Flask(__name__)                     # Flask 서버 생성
CORS(app)                                 # 모든 프론트 요청 허용

#-------------------------
# DB 연결 + 테이블 생성
#-------------------------
conn = sqlite3.connect("schedule.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    time TEXT,
    note TEXT
)
""")
conn.commit()

#-------------------------
# 일정 등록 API (Create)
#-------------------------
@app.route('/add_schedule', methods=['POST']) # 프론트가 POST 방식으로 요청함
def add_schedule():
    data = request.get_json()             # 프론트(HTML/JS) 에서 JSON 받아오기
    title = data['title']                 # 일정 제목
    date = data['date']                   # 일정 날짜
    time = data['time']                   # 일정 시간
    note = data['note']                   # 메모
    
    cur.execute(
        "INSERT INTO schedule (title, date, time, note) VALUES (?, ?, ?, ?)",
        (title, date, time, note)
    )
    conn.commit()
    
    return jsonify({"message": "일정이 DB에 추가되었습니다!"})

#-------------------------
# 일정 목록 조회 API (Read)
#-------------------------
@app.route('/get_schedule')
def get_schedule():
    cur.execute("SELECT * FROM schedule")
    rows = cur.fetchall()
    
    schedules = []
    for r in rows:
        schedules.append({
            "id": r[0],
            "title": r[1],
            "date": r[2],
            "time": r[3],
            "note": r[4]
        })

    return jsonify({"schedule": schedules})

#-------------------------
# 일정 삭제 기능
#-------------------------
@app.route('/delete_schedule', methods=['POST'])
def delete_schedule():
    data = request.get_json()
    schedule_id = data['id']
    
    cur.execute("DELETE FROM schedule WHERE id=?", (schedule_id,))
    conn.commit()
    
    return jsonify({"message": "일정 삭제 완료!"})
        
#-------------------------
# 일정 수정 기능
#-------------------------
@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    data = request.get_json()

    schedule_id = data['id']
    title = data['title']
    date = data['date']
    time = data['time']
    note = data['note']
        
    cur.execute("""
        UPDATE schedule
        SET title=?, date=?, time=?, note=?
        WHERE id=?
    """, (title, date, time, note, schedule_id))
    conn.commit()
        
    return jsonify({"message": "일정 수정 완료!"})

#-------------------------
# 서버 실행
#-------------------------
if __name__ == "__main__":
    app.run(debug=True)