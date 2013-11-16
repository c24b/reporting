#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from urlparse import urlparse
#parsing
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
import re
from webscraping import webkit
#connexion lib
import requests
import json

	
def statigr(self):
	'''simple extraction of statigram 
	that already use INSTAGRAM API
	*stat of user:
		- media, follower, following
	*stat per image:
		-like, comment, favorite pict
	'''
	self._values = {}
	dict_img = {}
	for n in bs(self._content).findAll("div", {"class":re.compile('^user.*?$')}):
		for n in zip(n.findAll("span",{"class":"chiffre"}), n.findAll("span",{"class":"legende"})):
			self._values[n[1].get_text()] = int((n[0]).get_text())	
	for n in bs(self._content).findAll("div", {"id":re.compile('^detailPhoto.*?$')}):
		for img in n.findAll('span'):
			dict_img[img.get('class')[0]] = img.get_text()
		self._values[n.find('img')['src']] = dict_img 		
	return self
	
def youtube(self):
	raise NotImplementedError
	#~ res =  bs(self._content).find("div", {"class":"spf-nolink"})
	#~ print res
	#~ print res.find_all("a")
	#~ #print bs(self._content).find_all({"div", {"class":"spf-nolink"})
	#~ video1 =  bs(self._content).find("div", {"id": "watch-view-count "}).text
	#~ print video1
	#~ self._values = re.sub(r"\D","",video1)
	#~ return self
			

def twitter(self):
	self._values = {}
	res = bs(self._content).find('ul', {'class':'stats'})
	for n in res.find_all('li'):
		self._values[re.sub(" ","", n.strong.nextSibling).lower()] = re.sub(r"\D","",n.strong.get_text()) 
	return self
	

def facebook(self):
	self._values = {}
	n = bs(self._content).find_all('code')
	if n is not None:
		res = (n[2].string).encode("utf-8")
		like = re.split("class\=\"fsm.fwn.fcg\"\>|·|\<\/div\>\<\/div\>\<\/h2\>", res)
		self._values['likes'] = (re.sub(r"\D","", like[2]))
		self._values['talking'] = (re.sub(r"\D","", like[3]))
	else:
		pass
	return self


class Connexion(object):
	''' 
	basic wrapper around python requests: fetching content providing a url 
	*fetch with multiples options : 
	- timeout (defaut = 5)
	- dict proxies (defaut = {})
	- dict headers for User-Agent (defaut = {'User-Agent': 'Mozilla/5.0',})
	- Retries (defaut 2)
	*check status information:
	- status_code
	- redirect
	'''
	def __init__(self, url, timeout=5, proxies ={}, headers = {'User-Agent': 'Mozilla/5.0',}, retry = 2, redir=True, ):
		self._timeout = timeout
		self._proxies = proxies
		self._headers = headers
		self._url = url
		self._active_redir = redir
		self._content = None
		self._status_code = None
		self._redirect = None
		self._retries = retry
		
	def fetch(self):
		requests.adapters.DEFAULT_RETRIES = self._retries
		#headers = {
		#	'User-Agent': 'Mozilla/5.0',
		#}
		try:
			print self._url
			r = requests.get(self._url, headers = self._headers,allow_redirects=self._active_redir,timeout=self._timeout, proxies=self._proxies)
			#, allow_redirects=self._redirect, 
			self._content = r.text
			self._status_code = r.status_code
			self._redirect = r.history
		except requests.exceptions.ConnectionError:
			self._status_code = 404
		return self
		
	def check(self):
		
		if self._status_code != 200:
			self._status = False
			return self
			
		elif len(self._redirect) > 0: 
			self._status = False
			return self
			
		elif self._status_code == 200:
			self._status = True
			return self
		else:
			self._status = False
			return self

class Page(Connexion):
	'''simple function to dispatch treatement according to the type of Ressources'''
	def __init__(self, url):
		Connexion.__init__(self, url)
		self._values = None
	
	def get_type(self):
		'''
		define sourcetype by parsing netloc and retrieving domain name without extension
		with or without the www.
		'''
		try:
			self._type =(urlparse(self._url).netloc).split(".")[-2]
			
		except IndexError:
			self._status = False
	def dispatch(self):
		'''
		mini dispatcher de méthode d'extractions en fonction du type de ressource
		'''
		
		self.get_type()
		if self._type != None:
			self.fetch()
			try:
				getattr(sys.modules[__name__],self._type)(self)
			except AttributeError:
				print "Extractor not implemented for %s" %self._type 
			
		else:
			return "Not Implemented"

if __name__ == '__main__':
		msg = Page()
		msg.dispatch()
		print msg._values
