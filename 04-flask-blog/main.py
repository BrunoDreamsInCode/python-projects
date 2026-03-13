from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_posts_data():
    response = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391")
    response.raise_for_status()
    posts_data = response.json()

    return posts_data



@app.route('/')
def home():
    posts_data = get_posts_data()

    return render_template("index.html", all_posts=posts_data)


@app.route('/blog/<int:post_id>')
def show_post(post_id):
    posts = get_posts_data()

    for post in posts:
        if post["id"] == post_id:
            return render_template("post.html", post=post)
    return f"Post not found"



if __name__ == "__main__":
    app.run(debug=True)