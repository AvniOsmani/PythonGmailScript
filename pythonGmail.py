# compile and run with
# python pythonGmail.py

# This program reads all of your unread emails in your inbox,
# reads the guessed number from the subject and reads the name from the sender's email address,
# then sends an email to each person, the subject tells them if they guess the number correctly,
# and the body of the email has a youtube link that searches the sender's name in youtube.

# The emails in the inbox should not contain anything in the body of the message and the subject should only contain a number.
# You can use the following email to test because we have allowed "less secure apps" to the gmail account.

#replace everywhere you see ***GMAIL ADDRESS*** with your gmail address and ***GMAIL PASSWORD*** with your password


import poplib
import string, random
import StringIO, rfc822
import logging
import random
import smtplib
import imaplib
import email
import operator
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from itertools import chain
import os
import re, csv
import urllib2
from  urllib import urlencode, quote
import sys
reload(sys)
sys.setdefaultencoding('utf8')

SERVER = "pop.gmail.com"
USER  = "***GMAIL ADDRESS***"
PASSWORD = "***GMAIL PASSWORD***"

def Sendmail(toaddr, message):
	#html youtube search using the sendeer's name
        SearchStr = toaddr.split("@")[0]
	query= urlencode({"search_query" : toaddr.split("@")[0]})
	html = urllib2.urlopen("http://www.youtube.com/results?" + query)
	result = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode())
	body = ("http://www.youtube.com/watch?v=" + result[0])

	#sends the email
	fromaddr = "***GMAIL ADDRESS***"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = message

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "***GMAIL PASSWORD***")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


#connect to server
logging.debug('connecting to ' + SERVER)
server = poplib.POP3_SSL(SERVER)

#login to email
logging.debug('logging in')
server.user(USER)
server.pass_(PASSWORD)


x= random.randint(0, 10)
print ('The random number is:'),
print x
logging.debug('listing emails')
resp, items, octets = server.list()
gmail=imaplib.IMAP4_SSL('imap.gmail.com',993)
gmail.login(USER,PASSWORD)
gmail.list()
t=gmail.select('Inbox')
typ,data=gmail.search(None,'ALL')
email_list = []

#determines which emails are new emails
typ,unseenm= gmail.search(None,'UNSEEN')
ty,seenm=gmail.search(None,'SEEN')
maxseen=None
maxunseen= None
print unseenm
print seenm
if(seenm==['']):
   seenr= '0'
else:
	for n in seenm:
             if n > maxseen:
	            maxseen=n
	maxseen=maxseen.split()
	value= max(enumerate(maxseen))
	seenr=max(value)

if(unseenm==['']):
   unseenr=seenr
else:
	for u in unseenm:
	     if u > maxunseen:
                    maxunseen= u
	maxunseen=maxunseen.split()
	v= max(enumerate(maxunseen))
	unseenr=max(v)
num=0
counter=0

#only reads the unread emails
for num in range(int(seenr),int(unseenr)):

		id, size = string.split(items[num])
		resp, text, octets = server.retr(id)
		text = string.join(text, "\n")
		file = StringIO.StringIO(text)
		message = rfc822.Message(file)
		f= open("subjectinfo.txt","w+")
		f.write(message['subject'])
		f.close()
		f= open("subjectinfo.txt", "r")
		if f.mode == 'r':
        		content=f.read()
		#print content
		if content==str(x):
       			Sendmail(message['From'], "NOT SPAM!! YOU WIN!!!!! "+" My number was " + str(x))
			print (message['From'])
			counter+=1

		else:
			Sendmail(message['From'], "NOT SPAM!! SORRY, YOU LOOSE! "+" My number was " + str(x))


print counter,
print ('people guessed the random number correctly')

# marks all of the unread emails as read
if(int(unseenr)-int(seenr)>=1):
	obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
	obj.login(USER,PASSWORD)
	obj.select('Inbox')
	typ ,data = obj.search(None,'UnSeen')
	obj.store(data[0].replace(' ',','),'+FLAGS','\Seen')

#list all emails once in a file
e=open("emailList.txt","w+")
ids = data[0]
id_list = ids.split()
e= open("emailList.txt","w+")
for i in id_list:
	typ, data = gmail.fetch(i,'(RFC822)')
	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_string(response_part[1])
			sender = msg['from'].split()[-1]
			address = re.sub(r'[<>]','',sender)
	if not re.search(r'' + re.escape(USER),address) and not address in email_list:
		email_list.append(address)

		print address
		e.write(address+'\n')
e.close()
