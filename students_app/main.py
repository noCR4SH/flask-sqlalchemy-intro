from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuration for our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# Creation of SQLAlchemy object. We are passing the Flask app object here
db = SQLAlchemy(app)

# Creating a table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)

# Creating a route
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Creating a route for adding a student and handling the form
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    # Checking if the request method is POST
    if request.method == 'POST':
        # Getting data from form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']

        # Adding data to database

        # Creating new row before sending it to database
        new_student = Student(first_name=first_name, last_name=last_name, birthdate=birthdate)

        # Adding new_student to session
        db.session.add(new_student)

        # Submitting the session to database (saving to db)
        db.session.commit()

        # Redirecting to the index page after adding the student using url_for - it is a function that generates the URL for the given endpoint
        return redirect(url_for('index'))
    return render_template('add_student.html')

# app_context - it is a context manager that allows us to access the application context. It is needed to create the tables in the database
with app.app_context():
    db.create_all()
app.run(debug=True)