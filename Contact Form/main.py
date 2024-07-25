from flask import Flask, render_template,request
import requests

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

def sendEmail(message = None, name = None, email = None, phone = None):
    import smtplib

    sender = "pelealex02@gmail.com"
    receiver = "pele_alex02@yahoo.com"
    password = "bjuk ydww rilv zsbe"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(user=sender, password=password)
        connection.sendmail(
            from_addr=sender,
            to_addrs=receiver,
            msg='Subject:Hello, Mihnea\n'
                f'\n{message}'
                f'\n{name}'
                f'\n{email}'
                f'\n{phone}'
        )


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST","GET"])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", msg_sent=False)
    elif request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        sendEmail(name = name, email=email, phone=phone,message=message)
        return render_template("contact.html", msg_sent=True)

# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     if request.method == 'POST':
#         return "<h1> Successfully sent your message </h1>"

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
