import os

from flask import Flask, session, render_template, request, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine,Table, MetaData, Column, String, Integer, text
from sqlalchemy.orm import scoped_session, sessionmaker
from Book import import_books

app = Flask(__name__)

os.environ["DATABASE_URL"] = "postgresql://postgres:dataBasing@localhost:5433/postgres"
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True, nullable=False),
    Column('password', String, nullable=False)
)

# Create tables
metadata.create_all(engine)


def is_logged_in():
    return 'username' in session and session['username'] is not None

def username_exists(db, username):
    # Check if the username already exists in the database
    result = db.execute(text("SELECT COUNT(*) FROM users WHERE username = :username"), {"username": username}).scalar()
    return result > 0

def update_users(db, username, password):

    if username_exists(db, username):
        return


    count_query = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    current_count = count_query + 1  # Increment for the new record

    # Insert the new record
    insert_query = text("INSERT INTO users (username, password, id) VALUES (:username, :password, :id)")
    db.execute(insert_query, {"username": username, "password": password, "id": current_count})
    db.commit()
    return

def search_books(search_query):
    query = f"%{search_query}%"
    results = db.execute(
        text('SELECT * FROM books WHERE title ILIKE :query OR author ILIKE :query OR isbn ILIKE :query OR CAST(year AS VARCHAR) ILIKE :query'),
        {"query": query}
    ).fetchall()
    return results


# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Insert user data into the database
        update_users(db,username, password)
        session["username"] = username
        return render_template("search.html", user_val = True)

    return render_template("register.html")

# Route for user logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route("/book/<int:book_id>")
def book(book_id):
        # Fetch book details
        book_details = db.execute(text("SELECT * FROM books WHERE id = :book_id"), {"book_id": book_id}).fetchone()

        # Fetch reviews for the book
        # reviews = db.execute(text("SELECT * FROM reviews WHERE book_id = :book_id"), {"book_id": book_id}).fetchall()

        return render_template("book.html", book=book_details)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("search_query")

        if search_query:
            results = search_books(search_query)
            return render_template("search.html", results=results, search_query=search_query)
        else:
            flash("Please enter a search query.", "danger")

    return render_template("search.html")
# Route for the main page
@app.route("/")
def index():
    if is_logged_in():
        return render_template("index.html",user_val = True)
    else:
        session.pop('username', None)

        return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)