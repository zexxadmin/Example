from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Load or create config.json
def load_users():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

def save_users(users):
    with open('config.json', 'w') as f:
        json.dump(users, f)

# Generate a random account number
def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

# Home route (Landing page)
@app.route('/')
def home():
    if 'username' in session:  # Check if user is logged in
        return redirect(url_for('dashboard', username=session['username']))
    return redirect(url_for('signin'))  # Redirect to sign in if not logged in

# Sign Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        
        # Create new user
        account_number = generate_account_number()
        user = {
            "username": username,
            "password": password,
            "account_number": account_number,
            "balance": 0
        }
        users['users'].append(user)
        save_users(users)
        
        # Log the user in by starting a session
        session['username'] = username
        
        return redirect(url_for('dashboard', username=username))
    
    return render_template('signup.html')

# Sign In Route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Check if user exists
        user = next((u for u in users['users'] if u['username'] == username and u['password'] == password), None)
        
        if user:
            # Log the user in by starting a session
            session['username'] = username
            return redirect(url_for('dashboard', username=username))
        else:
            return "Invalid username or password"
    
    return render_template('signin.html')

# Dashboard Route
@app.route('/dashboard/<username>')
def dashboard(username):
    users = load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)
    if user:
        return render_template('home.html', user=user)
    return "User not found"

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session
    return redirect(url_for('signin'))

# Other routes for sending, receiving, and adding funds
@app.route('/send/<username>')
def send(username):
    return render_template('send.html', username=username)

@app.route('/receive/<username>')
def receive(username):
    return render_template('receive.html', username=username)

@app.route('/addfunds/<username>')
def addfunds(username):
    return render_template('addfunds.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)