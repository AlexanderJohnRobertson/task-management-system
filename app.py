from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, request
import os
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername

@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                # cur = mysql.connection.cursor()
                # cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user = cur.fetchall()
                cur.close()
                User = user[0]
                Uname = User[0]
                Pword = User[1]
                if Uname == username and Pword == password:
                    global_var(Uname)
                    return redirect(url_for('userhome', globalUsername = Uname))
                else:
                    # globalAttempt = global_var2(globalAttempt)
                    flash('Username or Password is incorrect!')
                    # print(globalAttempt)
            except IndexError:
                # globalAttempt = global_var2(globalAttempt)

                flash('Username or Password is incorrect!')
                # print(globalAttempt)
    return render_template('login.html')

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('createaccount.html')

@app.route('/userhome/<globalUsername>')
def userhome(globalUsername):
    globalUsername = globalUsername
    return render_template('userhome.html', globalUsername = globalUsername)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
