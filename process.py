import sys
import os
import re
import smtplib

def sendEmail(content):
	fromaddr = 'tim.crilly@gmail.com'
	toaddrs  = 'tim.crilly@boardworks.co.uk'
	msg = content
	username = 'tim.crilly@gmail.com'
	password = 'C0ffeecup'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

outbox_path = "/home/pi/author/outbox"
files = []
# get any files in the outbox and email them files = []

for (dirpath, dirnames, filenames) in os.walk(outbox_path):
	files.extend(filenames)
	# doing only top level so break after first
	break

for fn in files:
	# open the file
	fullpath = os.path.join(outbox_path, fn)
	with open(fullpath, 'r') as content_file:
		content = content_file.read()
		print("Emailing " + fullpath)
		sendEmail(content)


sys.exit()



with open('data.txt', 'r') as content_file:
	content = content_file.readlines()
	print(content)

text = ''.join(content)
result = re.sub("Shift_R\n", "", text)
result = re.sub("period", ".", result)
result = re.sub("apostrophe", "'", result) 
result = re.sub("parenright", ")", result) 
result = re.sub("parenleft", "(", result) 
result = re.sub("colon", ":", result) 
result = re.sub("Tab", "\t", result) 
result = re.sub("numbersign", "&", result) 
result = re.sub("space", " ", result) 
result = re.sub("Return", "@", result) 
result = re.sub(".+\\nBackSpace\\n*", "", result) 
result = re.sub("\n", "", result) 
result = re.sub("@", "\n", result) 

with open('output.txt', 'w') as output_file:
	output_file.write(result);
