import validators
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import requests


#Create the database object
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

#Create the app
app = Flask(__name__)
#Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
#Initialize the app with the extension
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


#Define the model for database
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)

#Define the model for Form
class RatingForm(FlaskForm):
    rating = StringField(label='Your Rating out of 10 e.g. 7.5', validators=[DataRequired(), ])
    review = StringField(label='Your Review', validators=[Length(min=1, max=75)])
    submit = SubmitField(label='Done')

#CREATE TABLE
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie)).scalars()
    return render_template("index.html", movies=movies)

@app.route("/edit movie", methods = ["POST", "GET"])
def edit_movie():
    movie = db.get_or_404(Movie, request.args.get("id"))
    form = RatingForm(obj=movie)

    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

if __name__ == '__main__':
    app.run(debug=True)
