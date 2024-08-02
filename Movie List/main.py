from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import requests

# API key
API_KEY = "yourkey"
url = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Create the database object
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# Initialize the app with the extension
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# Define the model for database
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(1000))
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(500))
    img_url: Mapped[str] = mapped_column(String(1000), unique=True)


# Define the model for Form
class RatingForm(FlaskForm):
    rating = StringField(label='Your Rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[Length(min=1, max=75)])
    submit = SubmitField(label='Done')


class AddMovieForm(FlaskForm):
    movie_name = StringField(label='Enter the movie name', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')


# CREATE TABLE
with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/edit movie", methods=["POST", "GET"])
def edit_movie():
    movie = db.get_or_404(Movie, request.args.get("id"))
    form = RatingForm()

    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    movie = db.get_or_404(Movie, request.args.get("id"))
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.movie_name.data
        response = requests.get(url=url, params={"api_key": API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)

    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        response.raise_for_status()
        data = response.json()

        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"],
            rating=0.0,
            ranking=0,
            review=""
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
