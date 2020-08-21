from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo  # mongo
import flask_login  # handle user login
import os
from dotenv import load_dotenv  # load in .env files
from passlib.hash import pbkdf2_sha256

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
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(email):
    user = db.users.find_one({
        'email': email
    })

    # if the email exists
    if user:
        # create a User object that represents the user
        user_object = User()
        user_object.id = user["email"]
        user_object.account_id = user["_id"]
        # return the User object
        return user_object
    else:
        # if the email does not exist in the database, report an error
        return None


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
        'password': pbkdf2_sha256.hash(password)
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
    if user and pbkdf2_sha256.verify(password, user["password"]):
        # if the password matches, authorize the user
        user_object = User()
        user_object.id = user["email"]
        user_object.account_id = user["_id"]
        flask_login.login_user(user_object)

        # redirect to a page and says login is successful
        flash("Login successful", "success")
        return redirect(url_for('home'))

    # if the login failed, return back to the login page
    else:
        flash("Wrong email or password", "danger")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@flask_login.login_required
def profile():
    email = flask_login.current_user.id
    account_id = flask_login.current_user.account_id
    return f"Email = {email}, account_id={account_id}"


@app.route('/secret')
@flask_login.login_required
def secret():
    return "You are in top secret area"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
