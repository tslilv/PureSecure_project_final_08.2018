# Python code to illustrate Sending mail with attachments
# from your Gmail account
# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

FROM = 'tslil3v@gmail.com'


def send_email(to_addr, subject, body, attach_files):
    print ("bbb,", body)

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = FROM

    # storing the receivers email address
    msg['To'] = to_addr

    # storing the subject
    msg['Subject'] = subject

    for i in attach_files:
            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))

            # open the file to be sent
            filename = i
            attachment = open(filename, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(FROM, "AS1123zx")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(FROM, to_addr, text)

    # terminating the session
    s.quit()

    print ("bbb,", body)

send_email('tslil7v@gmail.com', 'try', "body", ['logo.jpg'])

