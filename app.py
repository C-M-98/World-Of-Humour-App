import os
import sqlite3
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, session, make_response, url_for
from flask_compress import Compress
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import re
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import base64
from jokeapi import Jokes
import asyncio
from PIL import Image
import sys


    # INSTALL FLASK
app = Flask(__name__)
compress = Compress(app)
@app.before_request
def handle_chunking():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

app.secret_key ='ABCDEF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['COMPRESS-LEVEL'] = 9
app.config['COMPRESS_MIN_SIZE'] = 50
db = SQLAlchemy(app)
app.config['MAX_CONTENT_LENGTH'] = sys.maxsize
db = sqlite3.connect("userdata.db")
cursor = db.cursor()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def insert_user(name, email, hash):
     connection = sqlite3.connect("userdata.db")
     cursor = connection.cursor()
     cursor.execute("INSERT INTO users(name, email, hash) VALUES (?, ?, ?)", (name, email, hash))
     connection.commit()
     connection.close()



async def print_joke():
    categories = request.form.getlist("category")
    blacklist = request.form.getlist("blacklist")
    joke_type = request.form.get("jokeType")
    j = await Jokes()  # Initialise the class
    joke = await j.get_joke(category=categories, blacklist=blacklist, joke_type=joke_type)
    return joke





# CHECK FOR THE LOGIN
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/getJoke", methods=["GET","POST"])
@login_required
def getJoke():
    if request.method == "POST":
        user_id = session["user_id"]
        connection = sqlite3.connect("userdata.db")
        cursor = connection.cursor()
        row = cursor.execute("SELECT * FROM users WHERE id =?", (user_id,)).fetchone()
        name = row[1]
        age = row[4]
        gender= row[7]
        photo_data = row[6]
        encoded_image = base64.b64encode(photo_data).decode("UTF-8")
        connection.close()

        if age >= 18 and gender == "Female":
            image1 = "/static/woman18+.jpg"
        elif age <18 and gender == "Female":
            image1 = "/static/woman18.jpg"
        elif age >=18 and gender =="Male":
            image1 = "/static/men18+.jpg"
        else:
            image1 = "/static/men18.jpg"
        joke_text = asyncio.run(print_joke())
        if "type" in joke_text and joke_text["type"] == "single":
            joke_text1 = joke_text["joke"]
            return render_template("jokehome1.html", joke_text1=joke_text1,image1=image1, age=age, gender=gender,
                               name=name,encoded_image=encoded_image)
        elif "type" in joke_text and joke_text["type"] == "twopart":
            joke_text1 = joke_text["setup"]
            joke_text2 = joke_text["delivery"]
            return render_template("jokehome.html", joke_text1=joke_text1, joke_text2=joke_text2,image1=image1, age=age, gender=gender,
                               name=name,encoded_image=encoded_image)

        return render_template("jokehome.html",image1=image1, age=age, gender=gender,
                               name=name,encoded_image=encoded_image)
    else:
        image1 = "/static/men18.jpg"
        return render_template("jokehome.html",image1=image1)

 # GET TO THE LOGON PAGE
@app.route("/")
def log_on():
    if request.method == "GET":
        image1 = '/static/login3.jpg'
        return render_template("logon.html", image1 = image1)


@app.route("/upload", methods = ["GET","POST"])
@login_required
def upload():
    if request.method == "POST":
        image_file = request.files["photoInput"]
        file_name = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        image_file.save(image_path)
        with open(image_path, "rb") as f:
            photo_data = f.read()
            encoded_image_data =base64.b64encode(photo_data).decode("UTF-8")

        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        age = int(request.form.get("age"))
        gender= request.form.get("gender")
        user_id = session["user_id"]
        if not all([ name, email, number, age, gender]):
            image1 = '/static/login2.jpg'
            flash("Please fill out all the fields below", "error")
            user_id = session["user_id"]
            connection =sqlite3.connect("userdata.db")
            cursor = connection.cursor()
            row = cursor.execute("SELECT * FROM users WHERE id =?", (user_id,)).fetchone()
            name = row[1]
            email = row[2]
            age = row[4]
            number =row[5]
            if row[6] is not None:
                image = row[6]
            encoded_image_data = base64.b64encode(image).decode("UTF-8")
            cursor.close()

            return render_template("profile.html", image1=image1, name=name, email=email, age=age, number=number, encoded_image_data=encoded_image_data)

        connection = sqlite3.connect("userdata.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET photo_path = ?,name =?, email = ?, age = ?, number = ?, gender =? WHERE id = ?",
                        (photo_data, name, email, age, number, gender, user_id),)
        connection.commit()
        connection.close()

        if age >= 18 and gender == 'Female':
            image1 = '/static/woman18+.jpg'
            return render_template("homeM18+.html",
                           name=name, age=age, gender=gender, image1=image1, encoded_image_data=encoded_image_data)

        elif age < 18 and  gender == 'Female':
            image1 = '/static/woman18.jpg'
            return render_template("home18.html", image1=image1, encoded_image_data=encoded_image_data,
                           name=name, age=age, gender=gender)

        elif age >= 18 and  gender == 'Male':
            image1 = '/static/men18+.jpg'
            return render_template("homeM18+.html", image1=image1, image_path = image_path, encoded_image_data=encoded_image_data,
                           name=name, age=age, gender=gender)

        elif age < 18 and  gender == 'Male':
            image1 = '/static/men18.jpg'
            return render_template("home18.html", image1=image1,encoded_image_data=encoded_image_data,
                           name=name, age=age, gender=gender)
        return render_template("profile.html")
    else:
        image1 = '/static/login2.jpg'
        user_id = session["user_id"]
        connection =sqlite3.connect("userdata.db")
        cursor = connection.cursor()
        row = cursor.execute("SELECT * FROM users WHERE id =?", (user_id,)).fetchone()
        name = row[1]
        email = row[2]
        cursor.close()
        if row[6] is not None:
            image = row[6]
            encoded_image_data = base64.b64encode(image).decode("UTF-8")
            return render_template("profile.html", name = name, email = email, image1 = image1, encoded_image_data=encoded_image_data)

        return render_template("profile.html", name = name, email = email, image1 = image1) #REMEMBER JINJA FOR THIS IN THE TEMPLATE

@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        image1 = '/static/login2.jpg'
        name = request.form.get("name")
        password = request.form.get("password")
        if not name:
            flash("Please enter a name", "error")
            image1 = '/static/login2.jpg'
            return render_template("login.html", image1 = image1)
        if not password:
            flash("Please enter a password", "error")
            image1 = '/static/login2.jpg'
            return render_template("login.html", image1 = image1)

        connection = sqlite3.connect("userdata.db")
        cursor = connection.cursor()
        row = cursor.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()


        if row is None or not check_password_hash(row[3],password):
            connection.close()
            flash("Invalid login details", "error")
            return render_template("login.html", image1 = image1)
        else:
            name = row[1]
            email = row[2]
            gender= row[7]
        if gender is not None:
            age = int(row[4])
            photo_path = row[6]
            encoded_image_data = base64.b64encode(photo_path).decode('UTF-8')
            number= row[5]

        session["user_id"] = row[0]
        connection.close()
        if not row[6]:
            return render_template("index.html", image1 = image1, name= name, email = email)
        elif age >= 18 and gender == 'Female':
            image1 = '/static/woman18+.jpg'
            return render_template('homeM18+.html', image1=image1, name=name, age=age, gender=gender, encoded_image_data=encoded_image_data)
        elif age < 18 and gender == 'Female':
            image1 = '/static/woman18+.jpg'
            return render_template('homeM18+.html', image1=image1, name=name, age=age, gender=gender, encoded_image_data=encoded_image_data)
        elif age >= 18 and gender == 'Male':
            image1 = '/static/men18+.jpg'
            return render_template('homeM18+.html', image1=image1, name=name, age=age, gender=gender, encoded_image_data=encoded_image_data)
        elif age < 18 and gender == 'Male':
            image1 = '/static/men18.jpg'
            return render_template('homeM18+.html', image1=image1, name=name, age=age, gender=gender, encoded_image_data=encoded_image_data)
        return render_template('index.html')

    else:
        session.clear()
        image1 = '/static/login2.jpg'
        return render_template("login.html", image1 = image1)



     #GO TO THE REGISTER PAGE
@app.route("/register", methods =["GET", "POST"])
def register():
        if request.method == "POST":
            image1 = '/static/login2.jpg'

            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            hash = generate_password_hash(password)

            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
               return render_template("register.html")
            if not name:
               return render_template("register.html")
            if password != confirm:
               flash("Paswords doesn't match", "error")
               return render_template("register.html", image1= image1)

            insert_user( name, email, hash)

            return render_template("login.html", image1 = image1)
        else:
            image1 = '/static/login2.jpg'
            return render_template("register.html", image1 = image1)

@app.route("/index", methods =["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
       image1 = '/static/login.jpg'
       return render_template("profile.html", image1 = image1)
    else:
        image1 = '/static/login.jpg'
        return render_template("index.html", image1 = image1)



