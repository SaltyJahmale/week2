from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from bleach import clean

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\dewijones\PycharmProjects\week2\data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

mode = 'safe'
# mode = ''

class Headers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_header = db.Column(db.TEXT())

@app.route('/')
def show_header():

    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    sql_string =  """ SELECT DISTINCT request_header, count(*) as Received 
                      FROM Headers 
                      GROUP BY request_header """

    result = conn.execute(sql_string)
    print("Retrieving successfully")

    return render_template('index.html', result=result)

@app.route('/add_header', methods=['POST'])
def add_header():

    if request.method == 'POST':
        if mode == 'safe':

            # Escaping data + no sql injection possible
            result = request.headers
            escape_data = clean(str(result))

            header_data = Headers(request_header=escape_data)

            db.session.add(header_data)
            db.session.commit()
        else:

            # SQL injection possible
            result = request.headers

            conn = sqlite3.connect('data.db')
            print("Opened database successfully")
            asd = str(result).replace('\n', '').replace('\r', '')

            sql_string = "INSERT INTO headers (request_header) VALUES ('"+ asd + "')"

            print(sql_string)
            conn.execute(sql_string)
            conn.commit()
            print("Inserted successfully")
            # conn.close()

    return redirect(url_for('show_header'))


if __name__ == '__main__':
    app.run(debug=True)