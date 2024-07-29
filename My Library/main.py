from flask import Flask, render_template, request, redirect, url_for
import sqlite3

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []
db = sqlite3.connect("books-collection.db")
cursor = db.cursor()

# cursor.execute("CREATE TABLE books "
#                "(id INTEGER PRIMARY KEY, "
#                "title varchar(250) NOT NULL UNIQUE, "
#                "author varchar(250) NOT NULL, "
#                "rating FLOAT NOT NULL)")

cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()



def to_dict(book_name, book_author, book_rating):
    book_dict = {
        "title": book_name,
        "author": book_author,
        "rating": book_rating
    }
    return book_dict


@app.route('/')
def home():
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book = request.form["book"]
        author = request.form["author"]
        rating = request.form["rating"]
        all_books.append(to_dict(book, author, rating))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
