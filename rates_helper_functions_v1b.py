import smtplib  # for sending automatic email
from email.mime.text import MIMEText  # for sending automatic email
from email.mime.multipart import MIMEMultipart  # for sending automatic email
from email.mime.application import MIMEApplication  # for sending automatic email
import pandas as pd
import pandas_datareader as pdr
import datetime
import os
import matplotlib


# Global variables:
cwd = os.getcwd()
today_str = datetime.datetime.today().strftime('%Y-%m-%d')
today_dtime = datetime.datetime.today()
now = datetime.datetime.now()
dtime_string = now.strftime("%Y-%m-%d-%H-%M-%S")
# dir_to_send = cwd + str('\\_TO_SEND_\\') + dtime_string + str('\\')
# os.mkdir(dir_to_send)


def send_mail_gmail(username, password, toaddrs_list,
                    msg_text, fromaddr=None, subject="Test mail",
                    attachment_path_list=None):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username, password)
    msg = MIMEMultipart()
    sender = fromaddr
    recipients = toaddrs_list
    msg['Subject'] = subject
    if fromaddr is not None:
        msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    if attachment_path_list is not None:
        os.chdir(attachment_path_list)
        files = os.listdir()
        for f in files:  # add files to the message
            try:
                file_path = os.path.join(attachment_path_list, f)
                attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
                attachment.add_header('Content-Disposition', 'attachment', filename=f)
                msg.attach(attachment)
            except:
                print("could not attach file")
    msg.attach(MIMEText(msg_text, 'html'))
    s.sendmail(sender, recipients, msg.as_string())

