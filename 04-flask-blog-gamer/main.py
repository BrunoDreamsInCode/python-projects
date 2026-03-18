from pprint import pprint

from flask import Flask, render_template
import requests, pprint
from six import raise_from

def get_all_posts():
    response = requests.get(url='https://api.npoint.io/0e145271c967686f2545')
    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data)
        return data

app = Flask(__name__)

@app.route("/")
def home():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/post/<slug>")
def post(slug):
    posts = get_all_posts()

    for post in posts:
        if post["slug"] == slug:
            return render_template("post.html", post=post)

    return "Post not found", 404



if __name__ == "__main__":
    app.run(debug=True)

