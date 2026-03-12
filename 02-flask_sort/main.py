from flask import Flask
import random

app = Flask(__name__)
random_number = random.randint(0,9)
print(f"debug: Número sortado: {random_number}")

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper


@app.route('/<int:guessed_number>')
def guess_message(guessed_number):
    if guessed_number == random_number:
        return (f'<h1 style="color:green;">You got it!</h1>'
                f'<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjQ3OXlrNXc3eDY4MnRnZ2l3aHdhcGp2aWZxZXU1c2dnaDRiOWU3ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zNbiX43QsqUAU/giphy.gif" width="400" height="400">')
    elif guessed_number > random_number:
        return (f'<h1 style="color:red;">Too high, try again!</h1>'
                f'<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDN2ZTN0b3lib29qMDRmc2l4amZmYjlxMG1ubjNpa2VqZGphZnAybCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fQoIDlLW6A6BAhyev8/giphy.gif" width="400" height="400">')
    else:
        return (f'<h1 style="color:purple;">Too low, try again!</h1>'
                f'<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzQ2b2tsd2JvcTh6cGhwbDF2MXBuZ3pkeHB0bHozZThxem9kZmFjNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/oO8Io8e7uHu8gJQYbg/giphy.gif" width="400" height="400">')


@make_bold
@app.route('/')
def home_page():
    return """
    <h1>How to play</h1>
    <ul>
      <li>Type a number in the URL</li>
      <li>Press Enter</li>
      <li>
        Follow the hints
        <ul>
          <li>Too high</li>
          <li>Too low</li>
        </ul>
      </li>
      <li>Keep guessing until you get it right!</li>
    </ul>
    <img src="/static/gifs/how_to_play.gif" width="400" height="400">
    """

if __name__ == "__main__":
    app.run(debug=True)