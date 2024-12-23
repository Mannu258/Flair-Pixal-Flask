from app import mail, Message, app

# Define the function to send the submission email
def Submission_Mail(name, email, number, select, message):
    with app.app_context():
        # Email details
        subject = "Submission Confirmation - Flair Pixal"
        sender_email = "flairpixal@gmail.com"  # Replace with your sender email
        bcc_emails = ["mishramandeep@outlook.com"]  # Add any additional BCC addresses here

        # Body of the email
        body = f"""
        Hi {name},

        Thank you for reaching out to us at Flair Pixal!

        We have received your submission and appreciate you taking the time to connect with us. Here are the details you provided:
        - Name: {name}
        - Email: {email}
        - Contact Number: {number}
        - Topic/Selection: {select}
        - Message: {message}

        Our team is currently reviewing your submission and will get back to you shortly. If you have any urgent questions or need immediate assistance, feel free to contact us at 9386090900.

        You can also visit our website for more updates: https://web.flairpixal.tech/.

        Thank you for choosing Flair Pixal. We look forward to assisting you!

        Best Regards,
        Flair Pixal Team
        Website: https://web.flairpixal.tech/
        Contact: 9386090900
        """

        # Create the email message
        msg = Message(
            subject=subject,
            sender=sender_email,
            recipients=[email],  # Email provided during submission
            bcc=bcc_emails  # Add the BCC addresses
        )
        msg.body = body

        # Send the email
        try:
            mail.send(msg)
            print(f"Email successfully sent to {email}")
            return True
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
            return f"{e}"
