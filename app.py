from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
<<<<<<< HEAD
=======
import os
>>>>>>> 377875c88f70cc1a4ac78d7ea4ddc6f1096501ea

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
<<<<<<< HEAD
    data = request.json
    new_user = User(telegram_id=data['telegram_id'], phone=data['phone'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(telegram_id=data['telegram_id']).first()
    if user and user.phone == data['phone']:
        login_user(user)
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/get_contacts', methods=['GET'])
@login_required
def get_contacts():
    if current_user.role == 'Менеджер холодных звонков':
        contacts = Baza.query.all()
    elif current_user.role == 'Менеджер теплых звонков':
        contacts = BazaGold.query.all()
    return jsonify([{'id': contact.id, 'contact': contact.contact, 'status': contact.status} for contact in contacts])

@app.route('/update_contact', methods=['POST'])
@login_required
def update_contact():
    data = request.json
    contact = Baza.query.get(data['id'])
    if contact:
        if data['status'] == 'интересно':
            new_contact = BazaGold(contact=contact.contact, status='подтверждено')
            db.session.add(new_contact)
        elif data['status'] == 'не интересно':
            new_contact = BazaCold(contact=contact.contact, status='не подтверждено')
            db.session.add(new_contact)
        db.session.delete(contact)
        db.session.commit()
    return jsonify({'message': 'Contact updated successfully'})
=======
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
>>>>>>> 377875c88f70cc1a4ac78d7ea4ddc6f1096501ea

if __name__ == '__main__':
    app.run(debug=True)
