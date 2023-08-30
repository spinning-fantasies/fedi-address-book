from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    sort_location = request.args.get('sort_location', 'asc')
    sort_created_at = request.args.get('sort_created_at', 'asc')

    if sort_location == 'asc':
        location_order = 'ASC'
    else:
        location_order = 'DESC'

    if sort_created_at == 'asc':
        created_at_order = 'ASC'
    else:
        created_at_order = 'DESC'

    cursor.execute(f'SELECT * FROM followers WHERE is_deleted = 0 ORDER BY location {location_order}, created_at {created_at_order}')
    followers = cursor.fetchall()

    conn.close()
    return render_template('index.html', followers=followers, sort_location=sort_location, sort_created_at=sort_created_at)



@app.route('/add_follower', methods=['GET', 'POST'])
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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
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
def delete(id):
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE followers SET is_deleted = 1 WHERE id = ?', (id,))
    conn.commit()

    cursor.execute('SELECT * FROM followers WHERE is_deleted = 0')
    followers = cursor.fetchall()

    conn.close()
    return render_template('index.html', followers=followers)

if __name__ == '__main__':
    app.run(debug=True)
