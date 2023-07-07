from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__, template_folder = 'templates')
app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rose_db'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('index.html')
    
# @app.route('/admin')
# def index():
#     return render_template('template.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/parameter')
def parameter():
    return render_template('parameter.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/user', methods=['GET'])
def user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users ')
    rows = cursor.fetchall()
    # data = Results(rows)

    return render_template('user.html', data=rows)

@app.route('/login')
def login():
    return render_template('login.html')









@app.route('/user', methods=['POST'])
def add_user():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('user.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
