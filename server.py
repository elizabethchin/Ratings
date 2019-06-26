"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html",
                            session=session)
   
@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register")
def register_form():
    """Make a new user with registration form."""

    return render_template("register_form.html")

@app.route("/register-process", methods=["POST"])
def register_process():
    """Register user, POST method."""
    
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    users = User.query.filter_by(email=email).all()
    length = len(users)
    
    if length == 0:
        name = User(email=email, password=password)
        db.session.add(name)
        db.session.commit()
        
    return redirect("/")

@app.route("/login")
def login_form():
    """Login page."""

    return render_template("login_form.html")

@app.route("/handle-login")
def handle_login():
    email = request.args.get("email")
    password = request.args.get("password")
    print(email)
    print(password)

    user = User.query.filter_by(email=email).first()
    if user != None and user.password == password:
        print("here")
        print(user.password)
        session["user"] = user.user_id
        flash("Logged in")
        return redirect("/")            
    else:
        flash("Wrong password")
        return redirect("/")

@app.route("/logout")
def logout():
    if "user" in session:
        session["user"] = None
        flash("Logged out")
    return redirect("/")

@app.route("/user-info")
def user_info():

    return render_template("user_info.html",
                            age=age,
                            zipcode=zipcode,
                            user=user)
      
# @app.route("user-info")
# def user_info():
#     pass




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
