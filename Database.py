from app import db,app,FormData

with app.app_context():
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
            return "Successfull"
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
            return "Successfull"
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
            return "Successfull"
            
            # return True
        except Exception as e:
            return e
