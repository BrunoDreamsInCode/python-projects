from flask import Flask, render_template, request, redirect, url_for
import pprint, sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
#Create the extension
db = SQLAlchemy(model_class=Base)
#Initialise the app with extension
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book id={self.id} title="{self.title}">'

    def __str__(self):
        return (f'ID: {self.id}\n'
                f'Title: {self.title}\n'
                f'Author: {self.author}\n'
                f'Rating: {self.rating}')

with app.app_context():
    db.create_all()


#CREATING (C)
def creating_book(name, author, rating):
    new_book = Book(title=name, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()


def reading_book():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return all_books


@app.route('/')
def home():
    all_books = reading_book()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        book_name = request.form.get("book_name")
        book_autor = request.form.get("book_autor")
        book_rating = request.form.get("book_rating")

        if not book_name or not book_autor:
            return render_template('error.html', message="All fields are required!", back_url="add")
        try:
            book_rating = float(book_rating)
            if not ( 0 <= book_rating <= 10):
                return render_template('error.html', message="Rating must be between 0 and 10", back_url="add")
        except(ValueError, KeyError):
            return render_template('error.html', message="Invalid rating value!", back_url="add")

        creating_book(book_name, book_autor, book_rating)
        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:id_book>", methods=["GET", "POST"])
def edit(id_book):
    book = db.session.execute(db.select(Book).where(Book.id == id_book)).scalar()

    if request.method == "POST":
        new_rating = request.form.get("new_rating")

        try:
            new_rating = float(new_rating)
            if not (0 <= new_rating <= 10):
                return render_template(
                    'error.html',
                    message="Rating must be between 0 and 10",
                    back_url="edit",
                    back_id=id_book
                )
        except (ValueError, TypeError):
            # valor não numérico
            return render_template(
                'error.html',
                message="Invalid rating value!",
                back_url=f"edit/{id_book}"
            )

        # se chegou até aqui, é válido
        book.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", book=book)


@app.route("/delete")
def delete():
    id_book = request.args.get("id_book")
    book = db.session.execute(db.select(Book).where(Book.id == id_book)).scalar()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)

