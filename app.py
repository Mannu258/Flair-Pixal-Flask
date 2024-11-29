from flask import Flask, render_template, request, send_from_directory
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
db = SQLAlchemy()
db.init_app(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "jeemannu90@gmail.com"
app.config["MAIL_PASSWORD"] = "icbh jolb cnuv dnbq"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)
mail.init_app(app)


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    number = db.Column(db.String(20))
    select_OR_SUBJECT = db.Column(db.String(100))
    message = db.Column(db.Text)

    def __repr__(self):
        return "<FormData %r>" % self.email



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        select = request.form.get("select")
        message = request.form.get("Message")
        if not select:
            cname = request.form.get("cname")
            cemail = request.form.get("cemail")
            cnumber = request.form.get("cnumber")
            csubject = request.form.get("csubject")
            cmessege = request.form.get("cmessage")
            from Database import save_conditional_form_data

            validate = save_conditional_form_data(cname, cemail, cnumber, csubject, cmessege)
            if validate=="True":
                pass
            else:
                return f"{validate}"

        from Database import save_main_form_data

        Validate = save_main_form_data(name, email, number, select, message)
        if Validate=="True":
            pass
        else:
            return f"{Validate}"
    if request.method == "GET":
        email = request.args.get("email")
        if email:
            from Database import save_single_email_form_data
            validate = save_single_email_form_data(email)
            if validate=="True":
                pass
            else:
                return f"{validate}"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
