from flask import Flask, render_template, request, flash, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import sqlite3
import json
import datetime
import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'yool'
auth = HTTPBasicAuth()

users = {
    os.getenv("USERNAME"): os.getenv("PASSWORD"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    sort_location = request.args.get('sort_location', 'desc')
    sort_created_at = request.args.get('sort_created_at', 'desc')

    if sort_location == 'asc':
        location_order = 'ASC'
    else:
        location_order = 'DESC'

    if sort_created_at == 'asc':
        created_at_order = 'ASC'
    else:
        created_at_order = 'DESC'

    cursor.execute(f'SELECT * FROM followers WHERE is_deleted = 0 ORDER BY  location {location_order}')
    followers = cursor.fetchall()

    conn.close()
    return render_template('index.html', followers=followers, sort_location=sort_location, sort_created_at=sort_created_at)

@app.route('/add_follower', methods=['GET', 'POST'])
@auth.login_required
def add_follower():
    if request.method == 'POST':
        created_at = request.form['created_at']
        display_name = request.form['display_name']
        account = request.form['acct']
        location = request.form['location']
        
        conn = sqlite3.connect('followers.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO followers (created_at, display_name, acct, location) VALUES (?, ?, ?, ?)',
                       (created_at, display_name, account, location))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_follower.html')

def update_database_with_new_followers(new_followers_data):
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    # Insert new data
    for follower in new_followers_data:
        cursor.execute('INSERT INTO followers (created_at, display_name, acct) VALUES (?, ?, ?)''', (follower['created_at'], follower['display_name'], follower['acct']))

    conn.commit()
    conn.close()

@app.route('/update_followers_list', methods=['GET', 'POST'])
@auth.login_required
def update_followers_list():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            file_content = file.read()
            try:
                new_followers_data = json.loads(file_content)
                update_database_with_new_followers(new_followers_data)
                flash('Followers list updated successfully!', 'success')
            except json.JSONDecodeError:
                flash('Invalid JSON format. Please upload a valid JSON file.', 'error')
        else:
            flash('Please upload a valid JSON file.', 'error')
    return render_template('update_followers_list.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@auth.login_required
def edit(id):
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM followers WHERE id = ?', (id,))
    follower = cursor.fetchone()

    if request.method == 'POST':
        location = request.form['location']
        display_name = request.form['display_name']

        cursor.execute('UPDATE followers SET location = ?, display_name = ? WHERE id = ?', (location, display_name,  id))
        conn.commit()

        cursor.execute('SELECT * FROM followers WHERE is_deleted = 0')
        followers = cursor.fetchall()

        conn.close()
        return render_template('index.html', followers=followers)

    conn.close()
    return render_template('edit.html', follower=follower)


@app.route('/delete/<int:id>')
@auth.login_required
def delete(id):
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE followers SET is_deleted = 1 WHERE id = ?', (id,))
    conn.commit()

    cursor.execute('SELECT * FROM followers WHERE is_deleted = 0')
    followers = cursor.fetchall()

    conn.close()
    return render_template('index.html', followers=followers)

if __name__ == "__main__":
    app.run(debug=True)
