import os
import csv
from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine,Table, MetaData, Column, String, Integer, text
from sqlalchemy.orm import scoped_session, sessionmaker

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


# Function to insert a book into the 'books' table
def insert_book(isbn, title, author, year):
    db.execute(text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)"),
               {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()

# Read data from CSV and insert into the 'books' table
def import_books():
    metadata = MetaData()
    books = Table('books', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('isbn', String, unique=True, nullable=False),
                  Column('title', String, nullable=False),
                  Column('author', String, nullable=False),
                  Column('year', Integer, nullable=False)
                  )
    metadata.create_all(engine)

    with open('books.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            isbn, title, author, year = row
            insert_book(isbn, title, author, int(year))

if __name__ == "__main__":
    import_books()