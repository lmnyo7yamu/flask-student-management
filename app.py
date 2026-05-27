from flask import (Flask, render_template, request, flash, redirect, url_for, Response)
import sqlite3 as sql
import csv
from io import StringIO

app = Flask(__name__)
# Secret key is required for flash messages
app.secret_key = "my_super_secret_key"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        nm = request.form['nm']
        age = request.form['age']  # Newly added field
        addr = request.form['add']
        city = request.form['city']
        pin = request.form['pin']

        # REQUIREMENT 3: Form Validation
        if not nm or not age or not addr or not city or not pin:
            flash("Error: All fields are required!", "error")
            return redirect(url_for('new_student'))

        # Check if PIN contains only numbers
        if not pin.isdigit():
            flash("Error: PIN code must contain only numbers!", "error")
            return redirect(url_for('new_student'))

        # Saving to database (Tutorial structure)
        try:
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, age, addr, city, pin) VALUES (?,?,?,?,?)",
                            (nm, age, addr, city, pin))
                con.commit()
                flash("Student successfully added!", "success")
        except Exception:
            con.rollback()
            flash("An error occurred during registration.", "error")
        finally:
            return redirect(url_for('list_students'))


@app.route('/list')
def list_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


# REQUIREMENT 5: Route for exporting CSV
@app.route('/export')
def export_csv():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    def generate():
        data = StringIO()
        writer = csv.writer(data)
        # Write headers
        writer.writerow(('Name', 'Age', 'Address', 'City', 'PIN'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        # Write data rows
        for row in rows:
            writer.writerow((row['name'], row['age'], row['addr'], row['city'], row['pin']))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # Trigger browser download
    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=students.csv"})


if __name__ == '__main__':
    app.run(debug=True)

