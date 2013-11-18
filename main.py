#!/usr/bin/env python
# -*- coding: utf-8 -*-


from reporter import Report
#from send_email2 import templating 


if __name__ == '__main__':
	r = Report()
	#r.tojson()
	print r.tohtml()
	
