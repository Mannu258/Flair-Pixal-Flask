# save this as app.py
from flask import Flask, render_template, request, send_from_directory
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "jeemannu90@gmail.com"
app.config["MAIL_PASSWORD"] = "icbh jolb cnuv dnbq"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)
mail.init_app(app)

with app.app_context():
    db.create_all()



@app.errorhandler(404)
def page_not_found(e):
    # Your custom logic here (logging, notifications, etc.)
    return render_template("404.html"), 404


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/about-us", methods=["POST", "GET"])
def About():
    return render_template("about.html")

@app.route("/what-we-do", methods=["POST", "GET"])
def Service():
    return render_template("about.html")

@app.route("/our-pricing", methods=["POST", "GET"])
def Price():
    return render_template("price.html")

@app.route("/contact-us", methods=["POST", "GET"])
def Contact():
    return render_template("contact.html")

@app.route("/get-quote", methods=["POST", "GET"])
def Quote():
    return render_template("quote.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)