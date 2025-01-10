from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    Response,
    send_file,
)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
import os
import datetime
from io import BytesIO

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
db = SQLAlchemy(app)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "flairpixal@gmail.com"
app.config["MAIL_PASSWORD"] = "jusl tfoo dpqr ddih"
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
        try:
            from Email import Submission_Mail

            status = Submission_Mail(name, email, number, select, message)
            if status:
                pass
            else:
                return f"{status}"
        except Exception as e:
            print(e)
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
        from Email import Submission_Mail

        status = Submission_Mail(cname, cemail, cnumber, csubject, cmessage)
        if status:
            pass
        else:
            return f"{status}"

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

            validate = save_conditional_form_data(
                cname, cemail, cnumber, csubject, cmessege
            )
            if validate == True:
                return render_template("Thank-you.html")
            else:
                return f"{validate}"

        Validate = save_main_form_data(name, email, number, select, message)
        if Validate == True:
            return render_template("Thank-you.html")
        else:
            return f"{Validate}"
    if request.method == "GET":
        email = request.args.get("email")
        if email:
            validate = save_single_email_form_data(email)
            if validate == True:
                pass
            else:
                return f"{validate}"
    return render_template("index.html")


@app.route("/qr-code-generator", methods=["GET", "POST"])
def qr_code_maker():
    if request.method == "POST":
        link = request.form.get("link")
        name = request.form.get("filename")

        if link:
            import qrcode
            from io import BytesIO
            from PIL import Image
            from ftplib import FTP

            try:
                # Generate QR code
                qr = qrcode.make(link)
                img_io = BytesIO()
                qr.save(img_io, format="PNG")
                img_io.seek(0)
                filename = f"{name}.png" if name else "qr_code.png"

                # Save QR code to a unique local file
                unique_filename = filename
                counter = 1
                while os.path.exists(unique_filename):
                    unique_filename = filename.replace(".png", f"_{counter}.png")
                    counter += 1

                with open(unique_filename, "wb") as f:
                    f.write(img_io.read())
                img_io.seek(0)  # Reset the BytesIO stream for the Response

                # FTP upload
                ftp = FTP("145.223.17.225")
                ftp.login("u172164904", "Mannu$123")
                ftp.cwd("domains/speechcare.in/Python/QR")

                # Create folder with today's date
                today_date = datetime.now().strftime("%Y-%m-%d")
                if today_date not in ftp.nlst():
                    ftp.mkd(today_date)

                ftp.cwd(today_date)

                # Check if file with the same name exists on FTP server
                file_exists = True
                ftp_unique_filename = unique_filename
                while file_exists:
                    try:
                        ftp.size(ftp_unique_filename)
                        # File exists, add a character to the filename
                        ftp_unique_filename = ftp_unique_filename.replace(
                            ".png", "a.png"
                        )
                    except:
                        # File does not exist
                        file_exists = False

                # Upload the file with the unique filename
                with open(unique_filename, "rb") as f:
                    ftp.storbinary(f"STOR {ftp_unique_filename}", f)
                ftp.quit()

                # Remove local file after upload
                os.remove(unique_filename)

                # Return the file for download
                return Response(
                    img_io.read(),
                    mimetype="image/png",
                    headers={
                        "Content-Disposition": f"attachment;filename={ftp_unique_filename}"
                    },
                )

            except Exception as e:
                return f"Error generating or uploading QR code: {str(e)}"
        else:
            return "Please enter a URL or text to generate a QR code."

    return render_template("QR.html")


@app.route("/youtube-video-downloader", methods=["GET", "POST"])
def youtube_video_downloader():
    if request.method == "POST":
        youtube_link = request.form.get("youtubeLink")

        if youtube_link:
            try:
                import yt_dlp as youtube_dl
                from ftplib import FTP

                # Create a folder named by the current date
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                save_path = os.path.join(os.getcwd(), current_date)  # Absolute path
                os.makedirs(save_path, exist_ok=True)

                # Download the YouTube video using yt-dlp
                ydl_opts = {
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'format': 'best'
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(youtube_link, download=True)
                    video_path = ydl.prepare_filename(info_dict)

                # Ensure the file name is unique locally
                base_name, ext = os.path.splitext(video_path)
                unique_video_path = video_path
                counter = 1
                while os.path.exists(unique_video_path):
                    unique_video_path = f"{base_name}_{counter}{ext}"
                    counter += 1
                os.rename(video_path, unique_video_path)
                video_path = unique_video_path

                # Generate a text filename based on the video name
                video_title = os.path.splitext(os.path.basename(unique_video_path))[0]
                txt_filename = f"{video_title}.txt"
                txt_file_path = os.path.join(save_path, txt_filename)

                # Save the link to a text file
                with open(txt_file_path, 'w') as file:
                    file.write(youtube_link)

                # FTP credentials
                ftp_host = "145.223.17.225"
                ftp_user = "u172164904"
                ftp_pass = "Mannu$123"
                ftp_directory = "domains/speechcare.in/Python/Youtube"

                # FTP upload
                ftp = FTP(ftp_host)
                ftp.login(ftp_user, ftp_pass)
                ftp.cwd(ftp_directory)
                if current_date not in ftp.nlst():
                    ftp.mkd(current_date)
                ftp.cwd(current_date)

                # Ensure the text file name is unique on the FTP server
                ftp_unique_txt_filename = txt_filename
                while ftp_unique_txt_filename in ftp.nlst():
                    base_name, ext = os.path.splitext(ftp_unique_txt_filename)
                    ftp_unique_txt_filename = f"{base_name}a{ext}"

                # Upload the text file
                with open(txt_file_path, "rb") as f:
                    ftp.storbinary(f"STOR {ftp_unique_txt_filename}", f)
                ftp.quit()

                # Remove local text file after upload
                os.remove(txt_file_path)

                # Return the video file for automatic download
                return send_file(video_path,
                                 mimetype='video/mp4',
                                 download_name=os.path.basename(video_path),
                                 as_attachment=True)

            except Exception as e:
                return f"Error saving or uploading the link, or downloading the video: {str(e)}"
        else:
            return "Please enter a YouTube link."

    return render_template("youtube.html")




@app.route("/admin")
def admin_dashboard():
    API = request.args.get("key", None)
    API_PASS = ["9386090900", "7017430421"]
    # http://127.0.0.1:8000/admin?key=9386090900
    if API in API_PASS:
        form_data = FormData.query.all()
        return render_template("Database.html", form_data=form_data)
    else:
        return redirect("/Error")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
