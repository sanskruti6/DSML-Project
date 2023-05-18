from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="bus_reservation"
)

# Create a cursor to interact with the database
cursor = db.cursor()

cursor.execute("USE bus_reservation")



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # Get the search parameters from the form
    source = request.form['source']
    destination = request.form['destination']
    date = request.form['date']

    # Query the database for available buses
    query = "SELECT * FROM buses WHERE source=%s AND destination=%s AND date=%s"
    cursor.execute(query, (source, destination, date))
    results = cursor.fetchall()

    return render_template('search.html', buses=results)


@app.route('/book', methods=['POST'])
def book():
    # Get the selected bus and passenger details from the form
    bus_id = request.form['bus_id']
    passenger_name = request.form['passenger_name']
    passenger_age = request.form['passenger_age']

    # Insert the booking details into the database
    query = "INSERT INTO bookings (bus_id, passenger_name, passenger_age) VALUES (%s, %s, %s)"
    cursor.execute(query, (bus_id, passenger_name, passenger_age))
    db.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
