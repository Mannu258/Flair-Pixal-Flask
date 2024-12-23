from flask import Flask, render_template, request, send_from_directory,redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
db = SQLAlchemy(app)


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
    email = db.Column(db.String(120))
    number = db.Column(db.String(20))
    select_OR_SUBJECT = db.Column(db.String(100))
    message = db.Column(db.Text)

    def __repr__(self):
        return "<FormData %r>" % self.email
    
with app.app_context():
    db.create_all()
    
    
def save_main_form_data(name, email, number, select, message):
    try:
        form_data = FormData(
            name=name,
            email=email,
            number=number,
            select_OR_SUBJECT=select,
            message=message,
        )
        db.session.add(form_data)
        db.session.commit()
        # return True
        return True
    except Exception as e:
        return e


def save_conditional_form_data(cname, cemail, cnumber, csubject, cmessage):
    try:

        form_data = FormData(
            name=cname,
            email=cemail,
            number=cnumber,
            select_OR_SUBJECT=csubject,
            message=cmessage,
        )
        db.session.add(form_data)
        db.session.commit()
        # return True
        return True
    except Exception as e:
        return e


def save_single_email_form_data(email):
    try:
        
        form_data = FormData(
            name="Single Email Submission",
            email=email,
            number="N/A",
            select_OR_SUBJECT="N/A",
            message="Single Email Submission",
        )
        db.session.add(form_data)
        db.session.commit()
        return True
    except Exception as e:
        return e




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

            validate = save_conditional_form_data(cname, cemail, cnumber, csubject, cmessege)
            if validate==True:
                return render_template('Thank-you.html')
            else:
                return f"{validate}"

        Validate = save_main_form_data(name, email, number, select, message)
        if Validate==True:
            return render_template('Thank-you.html')
        else:
            return f"{Validate}"
    if request.method == "GET":
        email = request.args.get("email")
        if email:
            validate = save_single_email_form_data(email)
            if validate==True:
                pass
            else:
                return f"{validate}"
    return render_template("index.html")


# @app.route("/admin")
# def Data():
#     API = request.args.get('API', None)
#     print(API)
#     API_PASS = ['9386090900','7017430421']
#     for i in API_PASS:
#         if i == API:          Simple logic

#             form_data = FormData.query.all()
#             return render_template('Database.html', form_data=form_data)
#         else:
#             return redirect("/Error")
    
    
@app.route("/admin")
def admin_dashboard():
    API = request.args.get('key', None)
    API_PASS = ['9386090900', '7017430421']
    # http://127.0.0.1:8000/admin?key=9386090900
    if API in API_PASS:
        form_data = FormData.query.all()
        return render_template('Database.html', form_data=form_data)
    else:
        return redirect("/Error")




if __name__ == "__main__":
    app.run(debug=True, port=8000)
