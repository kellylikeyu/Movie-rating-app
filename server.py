"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all-movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""  

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

# @app.route("/users")
# def all_users():
#     """View all movies."""

#     users = crud.get_users()

#     return render_template("all-users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")



@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular movie."""  

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html",user=user)


@app.route("/login", methods=["POST"])
def login_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Email and password do not match. Try again.")
    else:
        session["user.email"] = user.email 
        flash("Successfully logged in!")

    return redirect("/")    

@app.route("/movies/<movie_id>/ratings", methods=["POST"])    
def create_rating(movie_id):
    rating_num= request.form.get("rating")
    email = session.get("user.email")

    if "user.email" not in session:
        flash("You should Log in")
    else:     
        user = crud.get_user_by_email(email)
        movie = crud.get_movie_by_id(movie_id)
        rating = crud.create_rating(user,movie,int(rating_num))
        db.session.add(rating)
        db.session.commit()

    # rating = crud.create_rating_by_id(int(rating_num))
    return redirect(f"/movies/{movie_id}")  

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

