import api.configuration.globalVars as globalVars
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def emailRegistration(email):
    globalVars.init()
    msg = MIMEMultipart()
    msg['From'] = globalVars.emailUser
    msg['To'] = email
    msg['Subject'] = "eLab Registration Successful"
     
    body = "Your registration to eLab is now complete.  You are now eligible to be enrolled into the available courses."
    msg.attach(MIMEText(body, 'plain'))
      
    server = smtplib.SMTP(globalVars.emailServer, globalVars.emailPort)
    server.starttls()
    server.login(globalVars.emailUser, globalVars.emailPass)
    text = msg.as_string()
    try:
       server.sendmail(globalVars.emailUser, email, text)
       server.quit()
    except:
       pass


def emailEnroll(email, courseName):
    globalVars.init()
    msg = MIMEMultipart()
    msg['From'] = globalVars.emailUser
    msg['To'] = email
    msg['Subject'] = "eLab Enrollment Notification"
     
    body = "You have been enrolled into \"" + courseName + "\".  You may now login to eLab and access the associated content."
    msg.attach(MIMEText(body, 'plain'))
      
    server = smtplib.SMTP(globalVars.emailServer, globalVars.emailPort)
    server.starttls()
    server.login(globalVars.emailUser, globalVars.emailPass)
    text = msg.as_string()
    try:
       server.sendmail(globalVars.emailUser, email, text)
       server.quit()
    except:
       pass


def emailUnenroll(email, courseName):
    globalVars.init()
    msg = MIMEMultipart()
    msg['From'] = globalVars.emailUser
    msg['To'] = email
    msg['Subject'] = "eLab Unenrollment Notification"
     
    body = "You have been unenrolled from \"" + courseName + "\".  You no longer have access to the associated content."
    msg.attach(MIMEText(body, 'plain'))
      
    server = smtplib.SMTP(globalVars.emailServer, globalVars.emailPort)
    server.starttls()
    server.login(globalVars.emailUser, globalVars.emailPass)
    text = msg.as_string()
    try:
       server.sendmail(globalVars.emailUser, email, text)
       server.quit()
    except:
       pass
