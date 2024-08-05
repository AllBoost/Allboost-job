import sqlite3

DATABASE = 'allboost_job.db'

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.commit()
    con.close()
    return (rv[0] if rv else None) if one else rv

def register_employee(name, position):
    query_db('INSERT INTO employees (name, position) VALUES (?, ?)', [name, position])

def update_client_status(client_id, status, table):
    query_db(f'UPDATE {table} SET status = ? WHERE id = ?', [status, client_id])
