from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from db import init_db

app = Flask(__name__)
init_db(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "缺少用户名或密码"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409

    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "注册成功"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "登录成功"})
    return jsonify({"error": "用户名或密码错误"}), 401

@app.route("/")
def index():
    return "Auth API running."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
