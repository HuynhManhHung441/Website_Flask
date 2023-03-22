from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample user data for demonstration purposes
users = {
    'user1': {'password': 'pass1'},
    'user2': {'password': 'pass2'},
    'user3': {'password': 'pass3'}
}

@app.route('/')
def index():
    # Redirect to login page if user not authenticated
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'Hello, {session["username"]}! <a href="/logout">Logout</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect user to main page if already authenticated
    if 'username' in session:
        return redirect(url_for('index'))
    # On form submission, validate input credentials
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            session['username'] = username  # Set session variable to indicate successful login
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear session variable
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect user to main page if already authenticated
    if 'username' in session:
        return redirect(url_for('index'))
    # On form submission, validate input credentials
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        # Check if username already exists
        if username in users:
            return render_template('signup.html', error='Username already exists')
        # Add user to database
        users[username] = {'password': password}
        return redirect(url_for('login'))
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)