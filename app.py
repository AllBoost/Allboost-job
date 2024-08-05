from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Настройки для Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# Подключение к таблицам
name_sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1lV2aCAE5IbJo0Pl4wXp8u2LK4nvBQEE5y5N4hFXvQPM/edit?usp=sharing').sheet1
baza_sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1vzoTJnDwI5xuaLB8wsoftUtUyIqWgAOkrRDVuAwPIA0/edit?usp=sharing').sheet1
gold_sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1e40FaRT57BefEyBUEkd1RP6PHNnhqOdDcp_qthmlf5Q/edit?usp=sharing').sheet1
cold_sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1JtZcramnsz356AuUstZZNi_Mqbof97cVsbMBTLW7BbQ/edit?usp=sharing').sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        name_sheet.append_row([username, role])
        if role == 'cold':
            return redirect(url_for('cold_calls'))
        elif role == 'warm':
            return redirect(url_for('warm_calls'))
    return render_template('register.html')

@app.route('/cold_calls', methods=['GET', 'POST'])
def cold_calls():
    contacts = baza_sheet.get_all_records()
    if request.method == 'POST':
        contact_id = request.form['contact_id']
        status = request.form['status']
        contact = contacts[int(contact_id)]
        if status == 'interested':
            gold_sheet.append_row([contact['Name'], contact['Phone'], contact['Email']])
        else:
            cold_sheet.append_row([contact['Name'], contact['Phone'], contact['Email']])
    return render_template('cold_calls.html', contacts=contacts)

@app.route('/warm_calls', methods=['GET', 'POST'])
def warm_calls():
    contacts = gold_sheet.get_all_records()
    if request.method == 'POST':
        contact_id = request.form['contact_id']
        status = request.form['status']
        contact = contacts[int(contact_id)]
        if status == 'confirmed':
            teh_spec_sheet.append_row([contact['Name'], contact['Phone'], contact['Email']])
    return render_template('warm_calls.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
