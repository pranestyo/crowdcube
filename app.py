#!/usr/bin/env python3
from flask import *
import pymongo
import bcrypt
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "kudaliar78990"
uri = ("mongodb://localhost:27017")
client = MongoClient(uri)
db = client.crowd

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
	if "username" in session:
		return render_template('home.html')
	else:
		return redirect(url_for('index'))

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        cek = db.users.find_one({"username": username})
        if cek:
            hashed = str(cek['password'])
            if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
                session["username"] = username
                return redirect(url_for('home'))
            else:
                flash("Password Wrong")
                return redirect(url_for('login'))
        else:
            flash("Username Not Found")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))



if __name__ == "__main__":
	app.run(debug=True, use_reloader=True, host='0.0.0.0', port=1500)