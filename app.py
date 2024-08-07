from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50))

class Baza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20))

class BazaGold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20))

class BazaCold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20))

class TehSpec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(telegram_id=data['telegram_id'], phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/select_role', methods=['POST'])
def select_role():
    data = request.get_json()
    user = User.query.filter_by(telegram_id=data['telegram_id']).first()
    user.role = data['role']
    db.session.commit()
    return jsonify({"message": "Role selected successfully"}), 200

# Остальные маршруты для функционала

if __name__ == '__main__':
    app.run(debug=True)
