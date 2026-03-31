from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from api_movie import search_movie, get_movie_by_id


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Local db configuration - SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Table model for Movies.
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# Form used to update rating and review
class EditMovieForm(FlaskForm):
    new_rating = StringField("Your rating of 10 e.g 7.5", validators=[DataRequired()])
    new_review = StringField("Your review:",validators=[DataRequired()])
    submit = SubmitField("Done")

# Form used to search movies from API
class AddMovieForm(FlaskForm):
    new_movie = StringField("Title Movie:", validators=[DataRequired()])
    submit = SubmitField("Done")


@app.route("/")
def home():
    # Sort movies by rating (highest first)
    # Movies without rating appear at the end
    result = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc().nullslast())
    )
    all_movies = result.scalars().all()
    return render_template("index.html", all_movies=all_movies)

@app.route("/edit/<int:id_movie>", methods=["GET","POST"])
def edit(id_movie):
    movie = db.session.get(Movie, id_movie)
    form = EditMovieForm()
    if request.method == "POST":
        # Update user rating and review
        new_rating = request.form.get("new_rating")
        new_description = request.form.get("new_review")

        movie.rating = new_rating
        movie.review = new_description
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete/<int:id_movie>")
def delete(id_movie):
    movie = Movie.query.get(id_movie)
    if movie:
        # Delete movie from database
        db.session.delete(movie)
        db.session.commit()

        return redirect(url_for("home"))


@app.route("/add", methods=["GET","POST"])
def add():
    form = AddMovieForm()

    if request.method == "POST":
        # Search movies using external API based on user input
        movie_select = request.form.get("new_movie")
        movies = search_movie(movie_select)

        return render_template("select.html",  movies=movies)
    return render_template("add.html", form=form,)


@app.route('/select', methods=["GET","POST"])
def select():
    movie_api_id = request.args.get("id")

    if not movie_api_id:
        return redirect(url_for("add"))

    # Fetch full movie details from external API
    movie_data = get_movie_by_id(movie_api_id)

    # Create movie in database without rating (user will add it later)
    new_movie = Movie(
        title=movie_data["title"],
        img_url= f"https://image.tmdb.org/t/p/w500{movie_data['url_img']}",
        year=movie_data["year"],
        description=movie_data["description"]
    )

    db.session.add(new_movie)
    db.session.commit()

    # Redirect to edit page so user can add rating and review
    return redirect(url_for("edit", id_movie=new_movie.id))







if __name__ == '__main__':
    app.run(debug=True)
