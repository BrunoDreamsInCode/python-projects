from pprint import pprint
from dotenv import load_dotenv
from email.message import EmailMessage
from flask import Flask, render_template, request
import requests, pprint, smtplib, os




load_dotenv()

def send_form(name, email, tel, message):

    my_email = os.getenv("MY_EMAIL")
    my_password = os.getenv("APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "New Contact Form"
    msg["From"] = my_email
    msg["To"] = my_email
    msg["Reply-To"] = email

    msg.set_content(f"""
    Name: {name}
    Email: {email}
    Phone: {tel}

    Message:
    {message}
    """)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.send_message(msg)




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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        tel = request.form.get("tel")
        message = request.form.get("message")
        print(f"Name: {name}\nEmail: {email}\n Tel: {tel}\nMessage: {message}")

        send_form(name=name, email=email, tel=tel, message=message)
        return render_template("form_feedback.html", name=name, email=email, tel=tel, message=message)
    else:
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

