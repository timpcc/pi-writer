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
import json
import ConfigParser


class Mailer():
    
    def __init__(self):
        # load the username and password
        configPath = os.path.join("/home/pi/.config", "pi-writer", "email.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        acc = self.config.get("Email", "accounts");
        self.accounts = json.loads(acc)
        self.currentAccountIndex = 0
        self.recipients = self.config.get("Email", "recipients").split(";")
    
    def send(self, subject, message, files = []):
        try:
            COMMASPACE = ', '
            for i, acc in enumerate(self.accounts, self.currentAccountIndex):
                self.currentAccountIndex = i
                try:
                    if acc["auth"] == "tls":
                        smtp = smtplib.SMTP(acc["server"], acc["port"], timeout=30)
                        smtp.starttls()
                        print("enabled secure connection using TLS")
                    elif acc["auth"] == "ssl":
                        smtp = smtplib.SMTP_SSL(acc["server"], acc["port"], timeout=30)
                        smtp.set_debuglevel(True)
                    smtp.login(acc["user"], acc["password"])
                
                    send_to = COMMASPACE.join(self.recipients)
                    # construct message
                    msg = MIMEMultipart()
                    msg['From'] = acc["sender"]
                    msg['To'] = send_to
                    msg['Date'] = formatdate(localtime=True)
                    msg['Subject'] = subject
                
                    msg.attach( MIMEText(message) )
                
                    for f in files:
                        print("Adding file " + str(f))
                        part = MIMEBase('application', "octet-stream")
                        print("Created part")
                        part.set_payload( open(f,"rb").read() )
                        print("Set payload")
                        Encoders.encode_base64(part)
                        print("encoded as base64")
                        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                        print("added header")
                        msg.attach(part) 
                        print("attached")
                    print("Sending email...")
                    smtp.sendmail(acc["sender"], send_to, msg.as_string())
                    smtp.close()
                    print("Done.")
                    return True
                except Exception as ex:
                    # try next account
                    print(str(ex))
                    continue
            return False
        except Exception as e:
            print(str(e))
            return False