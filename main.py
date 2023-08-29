from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM followers WHERE is_deleted = 0')
    followers = cursor.fetchall()

    conn.close()
    return render_template('index.html', followers=followers)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('followers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM followers WHERE id = ?', (id,))
    follower = cursor.fetchone()

    if request.method == 'POST':
        email = request.form['email']

        cursor.execute('UPDATE followers SET email = ? WHERE id = ?', (email, id))
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
