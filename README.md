# Project 1 - Book Website 

## Overview

This project is a web app that is designed to allow users to register themselves with an account and then log in. They can search a database of books by name, author, ISBN, or date of publishing. The repository contains the two Python files that interface with the SQL and HTML to create this web app. There are 4 HTML files for each page used and one CSS file for the HTML styling. 

### File Structure

#### JPEGS

The photos are named HTMLPhoto(1-11). Note: Image 10 is missing.

#### Python Files 

1. **Book.py**
   - This is the application code that allows for the import of the book.csv file into the postgre sql database
   
1. **application.py**
   - This is the main application code that contains all the functions used for the web apps functionality

#### HTML Files

1. **Index.HTML**
   - This is the starting page when the webpage is accessed, it contains the navigation bar at the top allowing you to access the features of the web app.

2. **book.HTML**
   - This is the page that the user is brought to when they select a book from the search, it contains the book name, author, ISBN and date.

3. **resgister.HTML**
   - This is the page the user is brought to when they press the login button on the navigation bar, it interfaces with the database to either create an account or log them in.

4. **search.HTML**
   - This is the page the user is brought to when they press search or when they log in. It allows them to search the database for any of the books.

#### Stylesheets

1. **styles.css**
   - CSS stylesheet used for the HTML.
