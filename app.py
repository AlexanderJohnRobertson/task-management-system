from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, request, make_response
import os
import sqlite3
from sqlite3 import Error, IntegrityError, OperationalError
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername

@app.route('/', methods=['GET', 'POST'])
def index():
    # put application's code here
    cookie = request.cookies.get('userID')
    if cookie != "":
        resp = make_response(render_template('logoutcookie.html'))
        resp.set_cookie('userID', "")
        return resp
    else:
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
                    print(globalUsername)
                    user = Uname
                    resp = make_response(render_template('readcookie.html'))
                    resp.set_cookie('userID', user)
                    return resp
                    #return redirect(url_for('userhome', globalUsername = username))
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
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        accountType = "Standard"
        if not firstname:
            flash('First Name is required!')
        elif not lastname:
            flash('Last Name is required!')
        elif not username:
            flash('Username is required!')
        elif not email:
            flash('Email Address is required!')
        elif not phonenumber:
            flash('Phone Number is required!')
        elif not username:
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
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                cur.close()
                if user:
                    flash('Username already exists!')
                else:
                    if password != confirmPassword:
                        flash('Passwords do not match!')
                    else:
                        cur = conn.cursor()
                        cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)', (username, password, firstname, lastname, email, phonenumber, accountType))
                        conn.commit()
                        cur.close()
                        resp = make_response(render_template('readcookie.html'))
                        resp.set_cookie('userID', username)
                        return resp
                        #return redirect(url_for('userhome', globalUsername=username))
            except IndexError:
                flash('Username or Password is incorrect!')
    return render_template('createaccount.html')

@app.route('/userhome/', methods=['GET', 'POST'])
def userhome():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    #globalUsername = globalUsername
    #print("render userhome page")
    #print(type(globalUsername))
    name = request.cookies.get('userID')
    data = name
    print("Cookie: ", data)
    print(type(data))
    #return '<h1>welcome ' + name + '</h1>'
    return render_template('userhome.html', data=data)

@app.route('/viewtasks')
def viewtasks():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    data = cur.fetchall()

    #return jsonify(data)
    return render_template('viewtasks.html', data1=data)

@app.route('/viewprojects', methods=['GET', 'POST'])
def viewprojects():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects")
    data = cur.fetchall()
    print(data)
    print(type(data))

    #return jsonify(data)
    return render_template('viewprojects.html', data1=data)

'''@app.route('/readcookie', methods=['GET', 'POST'])
def readcookie():
    return redirect(url_for('userhome'))'''

@app.route('/addtask', methods=['POST', 'GET'])
def addtask():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    if request.method == 'POST':
        taskid = request.form['taskid']
        title = request.form['title']
        #description = request.form['description']
        duedate = request.form['duedate']
        priority = request.form['priority']
        status = request.form['status']
        projectid = request.form['projectid']
        description = request.form.get('description')
        print(taskid)
        print(title)
        print(description)
        print(duedate)
        print(priority)
        print(status)
        print(projectid)
        if not taskid:
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not duedate:
            flash('Due Date is required!')
        elif not priority:
            flash('Priority is required!')
        elif not status:
            flash('Status is required!')
        elif not projectid:
            flash('Project ID is required!')
        elif priority != 'High' and priority != 'Medium' and priority != 'Low':
            flash('Priority must be High, Medium, or Low!')
        elif status != 'Planned' and status != 'In Progress' and status != 'Completed' and status != 'Overdue' and status != 'Cancelled' and status !='Not Started':
            flash('Status must be Not Started, Planned, In Progress, Completed, Overdue or Cancelled!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,))
                task = cur.fetchall()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))
                project = cur.fetchall()
                cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
                user = cur.fetchall()
                if task:
                    flash('Task ID already exists!')
                elif not project:
                    flash('Project ID does not exist!')
                elif not user:
                    return render_template('accessdenied.html')
                else:
                    cur.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?)', (taskid, title, description, duedate, priority, status, projectid))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewtasks'))
            except IndexError:
                flash('Error adding task!')
            except IntegrityError:
                flash('Task ID already exists!')
            except OperationalError:
                flash('Database locked.')
                return redirect(url_for('addtask'))
    return render_template('addtask.html')

@app.route('/updatetask', methods=['POST', 'GET'])
def updatetask():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":
        return render_template('adminrequired.html')
    if request.method == 'POST':
        taskid = request.form['taskid']
        title = request.form['title']
        #description = request.form['description']
        duedate = request.form['duedate']
        priority = request.form['priority']
        status = request.form['status']
        projectid = request.form['projectid']
        description = request.form.get('description')
        print(taskid)
        print(title)
        print(description)
        print(duedate)
        print(priority)
        print(status)
        print(projectid)
        if not taskid:
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not duedate:
            flash('Due Date is required!')
        elif not priority:
            flash('Priority is required!')
        elif not status:
            flash('Status is required!')
        elif not projectid:
            flash('Project ID is required!')
        elif priority != 'High' and priority != 'Medium' and priority != 'Low':
            flash('Priority must be High, Medium, or Low!')
        elif status != 'Planned' and status != 'In Progress' and status != 'Completed' and status != 'Overdue' and status != 'Cancelled' and status !='Not Started':
            flash('Status must be Not Started, Planned, In Progress, Completed, Overdue or Cancelled!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,))
                task = cur.fetchall()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))
                project = cur.fetchall()
                if not task:
                    flash('Task does not exist!')
                elif not project:
                    flash('Project ID does not exist!')
                else:
                    cur.execute('UPDATE tasks SET title = ?, description = ?, duedate = ?, priority = ?, status = ?, projectID = ? WHERE taskID = ?', (title, description, duedate, priority, status, projectid, taskid))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewtasks'))
            except IndexError:
                flash('Error updating task!')
            except IntegrityError:
                flash('Task ID already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('updatetask.html')

@app.route('/deletetask', methods=['POST', 'GET'])
def deletetask():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":
        return render_template('adminrequired.html')
    if request.method == 'POST':
        taskid = request.form['taskid']
        title = request.form['title']
        print(taskid)
        print(title)
        if not taskid:
            flash('Task ID is required!')
        elif not title:
            flash('Title is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM tasks WHERE taskID = ?', (taskid,))
                task = cur.fetchall()
                if not task:
                    flash('Task does not exist!')
                elif task[0][1] != title:
                    flash('Task ID and Title do not match!')
                else:
                    cur.execute('DELETE FROM tasks WHERE taskID = ?', (taskid,))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewtasks'))
            except IndexError:
                flash('Error deleting task!')
            except IntegrityError:
                flash('Task ID already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('deletetask.html')

@app.route('/addproject', methods=['POST', 'GET'])
def addproject():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        print("User: ", user)
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    if request.method == 'POST':
        projectid = request.form['projectid']
        title = request.form['title']
        description = request.form.get('description')
        assignedTasks = request.form.get('assignedTasks')
        print(projectid)
        print(title)
        print(description)
        print(assignedTasks)
        if not projectid:
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not assignedTasks:
            flash('List of assigned tasks is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))
                project = cur.fetchall()
                if project:
                    flash('Project ID already exists!')
                else:
                    cur.execute('INSERT INTO projects VALUES(?, ?, ?, ?)', (projectid, title, description, assignedTasks))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewprojects'))
            except IndexError:
                flash('Error adding project!')
            except IntegrityError:
                flash('Project ID already exists!')
            except OperationalError:
                flash('Database locked.')
                return redirect(url_for('addproject'))
    return render_template('addproject.html')



@app.route('/updateproject', methods=['POST', 'GET'])
def updateproject():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":
        return render_template('adminrequired.html')
    if request.method == 'POST':
        projectid = request.form['projectid']
        title = request.form['title']
        description = request.form.get('description')
        assignedTasks = request.form['assignedTasks']

        print(projectid)
        print(title)
        print(description)
        print(assignedTasks)
        if not projectid:
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif not assignedTasks:
            flash('List of assigned tasks is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))
                project = cur.fetchall()
                if not project:
                    flash('Project does not exist!')
                else:
                    cur.execute('UPDATE projects SET title = ?, description = ?, tasks = ? WHERE projectID = ?', (title, description, assignedTasks, projectid))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewprojects'))
            except IndexError:
                flash('Error updating project!')
            except IntegrityError:
                flash('Project ID already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('updateproject.html')

@app.route('/deleteproject', methods=['POST', 'GET'])
def deleteproject():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    tupleUser = user[0]
    userType = tupleUser[6]
    if userType != "Administrator":
        return render_template('adminrequired.html')
    if request.method == 'POST':
        projectid = request.form['projectid']
        title = request.form['title']
        print(projectid)
        print(title)
        if not projectid:
            flash('Project ID is required!')
        elif not title:
            flash('Title is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM projects WHERE projectID = ?', (projectid,))
                project = cur.fetchall()
                if not project:
                    flash('Project does not exist!')
                elif project[0][1] != title:
                    flash('Project ID and Title do not match!')
                else:
                    cur.execute('DELETE FROM projects WHERE projectID = ?', (projectid,))
                    conn.commit()
                    cur.close()
                    #flash ('Task added successfully!')
                    return redirect(url_for('viewprojects'))
            except IndexError:
                flash('Error deleting project!')
            except IntegrityError:
                flash('Project ID already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('deleteproject.html')

@app.route('/changeusername', methods=['POST', 'GET'])
def changeUsername():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    if request.method == 'POST':
        username = request.form['username']
        newUsername = request.form['newUsername']
        confirmNewUsername = request.form['confirmNewUsername']
        password = request.form['password']
        print(username)
        print(password)
        print(newUsername)
        print(confirmNewUsername)
        if not username:
            flash('Username is required!')
        elif not newUsername:
            flash('New Username is required!')
        elif not confirmNewUsername:
            flash('Confirm New Username is required!')
        elif not password:
            flash('Password is required!')
        elif newUsername != confirmNewUsername:
            flash('New Username and Confirm New Username do not match!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                if not user:
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                else:
                    cur.execute('UPDATE users SET username = ? WHERE username = ?', (newUsername, cookie,))
                    conn.commit()
                    cur.close()
                    resp = make_response(render_template('readcookie.html'))
                    resp.set_cookie('userID', newUsername)
                    flash('Username changed successfully!')
                    #time.sleep(3)
                    return resp
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('changeusername.html')

@app.route('/changepassword', methods=['POST', 'GET'])
def changePassword():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        newPassword = request.form['newPassword']
        confirmPassword = request.form['confirmPassword']
        print(username)
        print(password)
        print(newPassword)
        print(confirmPassword)
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not newPassword:
            flash('New Password is required!')
        elif not confirmPassword:
            flash('Confirm New Password is required!')
        elif newPassword != confirmPassword:
            flash('New Password and Confirm New Password do not match!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                if not user:
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                else:
                    cur.execute('UPDATE users SET password = ? WHERE username = ?', (newPassword, cookie,))
                    conn.commit()
                    cur.close()
                    flash('Password changed successfully!')
                    return redirect(url_for('userhome'))
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('changepassword.html')

@app.route('/deleteaccount', methods=['POST', 'GET'])
def deleteAccount():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        print(username)
        print(password)
        print(confirmPassword)
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        elif not confirmPassword:
            flash('Confirm New Password is required!')
        elif password != confirmPassword:
            flash('Password and Confirm Password do not match!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                if not user:
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                else:
                    cur.execute('DELETE FROM users WHERE username = ?', (cookie,))
                    conn.commit()
                    cur.close()
                    flash('Account Deleted successfully!')
                    return redirect(url_for('index'))
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('deleteaccount.html')

@app.route('/accountdetails')
def viewAccountDetails():
    try:
        cookie = request.cookies.get('userID')
        print("Cookie", cookie)
        database = r"database.db"
        conn = None
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
        user = cur.fetchall()
        cur.close()
        if not user:
            return render_template('accessdenied.html')
    except IndexError:
        flash('Error')
    database = r"database.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (cookie,))
    data = cur.fetchall()
    tupleData = data[0]
    print(tupleData)
    tupleData = tupleData[0],tupleData[2],tupleData[3],tupleData[4],tupleData[5],tupleData[6]
    print(tupleData)
    print(type(tupleData))
    data = []
    data.append(tupleData)

    #return jsonify(data)
    return render_template('accountdetails.html', data1=data)

@app.route('/updateaccountdetails', methods=['POST', 'GET'])
def updateAccountDetails():
    cookie = request.cookies.get('userID')
    print("Cookie", cookie)
    database = r"database.db"
    conn = None
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
    user = cur.fetchall()
    cur.close()
    print("User: ", user)
    if not user:
        return render_template('accessdenied.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['updateFirstName']
        lastName = request.form['updateLastName']
        email = request.form['updateEmail']
        phoneNumber = request.form['updatePhoneNumber']
        print(username)
        print(password)
        print(firstName)
        print(lastName)
        print(email)
        print(phoneNumber)
        if not username:
            flash('Username is required!')
        elif not firstName:
            flash('First Name is required!')
        elif not lastName:
            flash('Last Name is required!')
        elif not email:
            flash('Email is required!')
        elif not phoneNumber:
            flash('Phone Number is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"database.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))
                user = cur.fetchall()
                tupleUser = user[0]
                if not user:
                    flash('User does not exist!')
                elif username != cookie:
                    flash('New Your username does not match your current username!')
                elif password != tupleUser[1]:
                    flash('Password is incorrect!')
                else:
                    cur.execute('UPDATE users SET forename = ?, surname = ?, email = ?, phone = ? WHERE username = ?', (firstName, lastName, email, phoneNumber, cookie,))
                    conn.commit()
                    cur.close()
                    flash('Account details updated successfully!')
                    return redirect(url_for('userhome'))
            except IndexError:
                flash('Error changing!')
            except IntegrityError:
                flash('User already exists!')
            #except OperationalError:
                #flash('Database locked.')
                #return redirect(url_for('updatetask'))
    return render_template('updateaccountdetails.html')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
