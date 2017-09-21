import smtplib

USER_EMAIL = "ourlkmteam@gmail.com"
PASSWORD = "lkmpass123"
RECIPIENT = "ourlkmteam@gmail.com"
SUBJECT = "Face detected"
BODY = "test mail BODY"


def send_email(body, user=USER_EMAIL, pwd=PASSWORD, recipient=RECIPIENT, subject=SUBJECT):

    print("Send mail called")

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


# send_email(USER_EMAIL, PASSWORD, RECIPIENT, SUBJECT, BODY)
