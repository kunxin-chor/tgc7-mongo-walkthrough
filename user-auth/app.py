from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo  # mongo
import flask_login  # handle user login
import os
from dotenv import load_dotenv  # load in .env files

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')

# set up the secret key to the Flask app
app.secret_key = SECRET_KEY

# connect to the Mongo database
client = pymongo.MongoClient(MONGO_URI)
db = client["sample_app"]


class User(flask_login.UserMixin):
    pass


# init the flask-login for our app
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/register')
def register():
    return render_template('register.template.html')


@app.route('/register', methods=["POST"])
def process_register():

    # extract out the email and password
    email = request.form.get('email')
    password = request.form.get('password')

    # TODO: Vadliate if the email and password are proper

    # Create the new user
    db.users.insert_one({
        'email': email,
        'password': password
    })

    flash("Sign up successful", "success")

    # Redirect to the login page
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.template.html')


@app.route('/login', methods=["POST"])
def process_login():
    # retrieve the email and the password from the form
    email = request.form.get('email')
    password = request.form.get('password')

    # check if the user's email exists in the database
    user = db.users.find_one({
        'email': email
    })

    # if the user exists, chec if the password matches
    if user and user["password"] == password:
        # if the password matches, authorize the user
        flask_login.login_user(user)

        # redirect to a page and says login is successful
        flash("Login successful", "success")
        return redirect(url_for('home'))

    # if the login failed, return back to the login page
    else:
        flash("Wrong email or password", "danger")
        return redirect(url_for('login'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
