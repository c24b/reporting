#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, json
from connect import *
from jinja2 import Template

class Report():
	def __init__(self, filename= "report.csv", report_title="report"):
		self._filename = filename
		self._title = report_title
		self._results = {}
	def csvReader(self):
		'''read url to extract from csv file'''
		file_handler = open(self._filename, "rb")
		with file_handler as f:
			csv_reader = csv.reader(file_handler, delimiter="\n")
			for row in file_handler:
				p = Page(row)
				p.dispatch()
				self._results[p._values['title']] = p._values 
		file_handler.close()
		return self

	def tohtml(self):
		self.csvReader()
		template = Template('''
		<ul>
		{% for key, value in data.items() recursive %}
			<a href="{{ value.url }}">{{ value.name }} - {{value.title }}</a>
			{%for k,v in value.stats.items() recursive %}
			<li>
				{{v}} <b>{{k}}</b>
			</li>	
		{% endfor %}
		{% endfor %}
		</ul>
		''')
		
		return template.render(data = self._results) 
	
	def tograph(self):
		raise NotImplementedError
	
	def tojson(self, sort = False):
		self.csvReader()
		return json.dumps(self._results, sort_keys= sort, indent=4)
	
	def toxls(self):
		raise NotImplementedError	
	def send(self, fromEmail, toEmail):
		raise NotImplementedError	
