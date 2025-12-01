from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("schedule.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    a = float(data['a'])
    b = float(data['b'])
    op = data['op']
    
    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        if b == 0:
            result = "0으로 나눌 수 없음"
        else:
            result = a / b
    else:
        result = "잘못된 연산"
        
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)