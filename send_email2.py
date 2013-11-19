#!/usr/bin/env python
# -*- coding: utf-8 -*-

#emailing
import smtplib
import MimeWriter
import mimetools
import cStringIO
    


class Email():
	def __init__(self, fromEmail, toEmail, subject, email_body):
		"""Create a mime-message that will render HTML in popular
			MUAs, text in better ones"""
		self._from = fromEmail
		self._to = toEmail
		self._title = subject
		self.txt_msg = email_body
		self._msg = email_body
		out = cStringIO.StringIO() # output buffer for our message 
		htmlin = cStringIO.StringIO(email_body)
		txtin = cStringIO.StringIO(email_body)

		writer = MimeWriter.MimeWriter(out)
		#
		# set up some basic headers... we put subject here
		# because smtplib.sendmail expects it to be in the
		# message body
		#
		writer.addheader("From", self._from)
		writer.addheader("Subject", self._title)
		writer.addheader("MIME-Version", "1.0")
		#
		# start the multipart section of the message
		# multipart/alternative seems to work better
		# on some MUAs than multipart/mixed
		#
		writer.startmultipartbody("alternative")
		writer.flushheaders()
		#
		# the plain text section
		#
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
		mimetools.encode(txtin, pout, 'quoted-printable')
		txtin.close()
		#
		# start the html subpart of the message
		#
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		#
		# returns us a file-ish object we can write to
		#
		pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
		mimetools.encode(htmlin, pout, 'quoted-printable')
		htmlin.close()
		#
		# Now that we're done, close our writer and
		# return the message body
		#
		writer.lastpart()
		self._msg = out.getvalue()
		out.close()
		return
		
	def send(self, server_addr, port, _login, _password):
		server = smtplib.SMTP(server_addr, port)
		server.starttls()
		server.ehlo()
		server.login(_login, _password)
		server.sendmail(_login, self._to, self._msg)
		server.quit()
		print "Message sent!"
		return 
