import requests
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash('your_password', method='pbkdf2:sha256')
print(hashed_password)
# Hashing password improves security and password theft, as even if hacker gets the password, it will be hashed (unique string) making it difficult to decipher

def query_llama(api_key, prompt):
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'prompt': prompt, 'max_tokens': 150}
    response = requests.post('https://api.llama3.com/v1/completions', headers=headers, json=data)
    return response.json()

# Create a Flask instance
app = Flask(__name__)
app.secret_key = 'kawhi'  # Required for session management

# Connect to SQLite3 database (or create it if it doesn't exist)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

# Home page route
@app.route('/')
def home():
    return render_template('home.html')


# Register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", (username, password, age))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = user[0]
            session['age'] = user[2]
            return redirect(url_for('welcome'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

# Welcome page route
@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        age = session['age']
        return render_template('welcome.html', username=username, age=age)
    else:
        return redirect(url_for('login'))

# Calculator page route
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operator = request.form['operator']
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error: Division by zero is undefined"
        else:
            result = "Invalid operator"
    return render_template('calculator.html', result=result)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



#  Main function to run the Flask app and initialise database
if __name__ == '__main__':
    init_db()  # calls the init_db() function to initialise
    app.run(port=5000, debug=True)
