from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'allboost_job.db'

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.commit()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        query_db('INSERT INTO employees (name, position) VALUES (?, ?)', [name, position])
        return jsonify({'status': 'success'}), 200
    return render_template('register.html')

@app.route('/manager/<string:position>', methods=['GET', 'POST'])
def manager(position):
    if position == 'cold':
        clients = query_db('SELECT * FROM clients')
    elif position == 'warm':
        clients = query_db('SELECT * FROM gold_clients')
    else:
        return "Invalid position", 400
    
    if request.method == 'POST':
        client_id = request.form['client_id']
        status = request.form['status']
        if position == 'cold':
            if status == 'interested':
                query_db('INSERT INTO gold_clients (name, status) SELECT name, status FROM clients WHERE id = ?', [client_id])
            query_db('INSERT INTO cold_clients (name, status) SELECT name, status FROM clients WHERE id = ?', [client_id])
        elif position == 'warm':
            if status == 'confirmed':
                query_db('INSERT INTO confirmed_clients (name, status) SELECT name, status FROM gold_clients WHERE id = ?', [client_id])
        return jsonify({'status': 'success'}), 200
    
    return render_template('manager.html', clients=clients, position=position)

if __name__ == '__main__':
    app.run(debug=True)
