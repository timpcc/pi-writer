'''
Created on 12 Dec 2013

@author: tim.crilly
'''
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import datetime
import shutil
import ConfigParser


class Mailer():
    
    def __init__(self, path):
        # load the username and password
        configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "email.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        self.server = self.config.get("Email", "server")
        self.user = self.config.get("Email", "user")
        self.password = self.config.get("Email", "password")
        self.sender = self.config.get("Email", "sender")
        self.recipients = self.config.get("Email", "recipients").split(";")
    
    def send(self, subject, message, files = []):

        COMMASPACE = ', '
        
        send_from = self.sender
        send_to = self.recipients
        username = self.user
        password = self.password
        
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'test'
        
        msg.attach( MIMEText("See attachment") )
        
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(f,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part) 
        #'smtp.gmail.com:587'
        smtp = smtplib.SMTP(self.server)
        smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()