from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'mydatabase'
mysql = MySQL(app)

@app.route('/')
def home():
    user = session.get('user_id')
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        price = request.form['price']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bus_routes (source, destination, departure_time, price) VALUES (%s, %s, %s, %s)",
                    (source, destination, departure_time, price))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('ticket_confirmation', source=source, destination=destination,
                                departure_time=departure_time, price=price))

    return render_template('bus_booking.html')

@app.route('/ticket_confirmation')
def ticket_confirmation():
    source = request.args.get('source')
    destination = request.args.get('destination')
    departure_time = request.args.get('departure_time')
    price = request.args.get('price')

    return render_template('ticket_confirmation.html', source=source, destination=destination,
                           departure_time=departure_time, price=price)

if __name__ == "__main__":
    app.run(debug=True)
