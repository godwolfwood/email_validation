from flask import Flask, request, redirect, render_template ,flash,session
import re
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)

app.secret_key = "twinjuan"
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'email_db')
# an example of running a query
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/process",methods=['POST'])
def process():
    email = request.form["email"]
    if not EMAIL_REGEX.match(email):
        flash("Email is not valid!")
        return redirect("/")
    query = "INSERT INTO users (users.email, users.created_at, users.updated_at) VALUE (:user_id , NOW() , NOW())"
    data = {
        "user_id": email
    }
    mysql.query_db(query,data)

    return redirect("/success")

@app.route("/success")
def success():
    emails = mysql.query_db("SELECT users.email as email, DATE_FORMAT(users.created_at,'%m/%d/%y %h:%i%p') as date FROM users")
    return render_template("success.html",emails=emails)

app.run(debug=True)