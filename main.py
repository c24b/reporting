#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reporter import Report

if __name__ == '__main__':
	r = Report()
	'''choose here the raw output format'''
	#r.json()
	#r.html()
	#r.graph() Not Implemented Yet 
	'''OR Directly send by mail to your buddies fullfiling the options'''
	''' USAGE:
	r.send(	mailserver='gmail', 
			port='80',
			_login="", 
			_password="",
			_from='youremail@mailbox.com', 
			_to=['dest1@mail.com', 'dest2@mail.com'], 
			title="Report by Labomatix", 
			format="html",)
	'''
	r.html()
	
