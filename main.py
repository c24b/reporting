#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib
from urlparse import urlparse
from requests.auth import HTTPBasicAuth
#parsing
from bs4 import BeautifulSoup as bs
from urlparse import urlparse
import re
from webscraping import webkit
#connexion lib
import requests
import json
from json import dumps, load
#data
import csv



def read_url(filename):
	file_handler = open(filename, "rb")
	with file_handler as f:
		csv_reader = csv.reader(file_handler, delimiter="\n")
		for row in file_handler:
			#print row
			p = Page(row)
			p.dispatch()
			print p._values['data']		
	file_handler.close()

def txt2int(n):
	try:
		return int(n)
	except ValueError:
		return n	

def statigr(self):
	'''simple extraction in json of statigram 
	url should begin by http://statigr.am/ to work 
	json data:
	* user:
		- url
		- stats : media, follower, following
	* data (list of every image limit to first load):
		-type
		-url
		- stats: like, comment, favorite pict
	=> Should directly take from instagram API :p
	'''
	user_stats_list = zip(bs(self._content).findAll("span",{"class":"chiffre"}), bs(self._content).findAll("span",{"class":"legende"}))
	
	#je mets à la ligne parce qu'on me dit que c'est illisible
	self._values['user'] = {"url":self._url, 
							"stats": dict((y.get_text(), x.get_text()) for x, y in user_stats_list)}
	self._values['data'] =[{
							'type':'img',
							'url':n.find('img')['src'],
							'stats':dict((img.get('class')[0], txt2int(img.get_text())) for img in n.findAll('span'))
							} 
							for n in bs(self._content).findAll("div", {"id":re.compile('^detailPhoto.*?$')})
							]
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
	res = bs(self._content).find('ul', {'class':'stats'})
	for n in res.find_all('li'):
		self._values[re.sub(" ","", n.strong.nextSibling).lower()] = re.sub(r"\D","",n.strong.get_text()) 
	return self
	

def facebook(self):
	n = bs(self._content).find_all('code')
	if n is not None:
		res = (n[2].string).encode("utf-8")
		like = re.split("class\=\"fsm.fwn.fcg\"\>|·|\<\/div\>\<\/div\>\<\/h2\>", res)
		self._values['likes'] = (re.sub(r"\D","", like[2]))
		self._values['talking'] = (re.sub(r"\D","", like[3]))
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
	def __init__(self, url, timeout=5, proxies ={'http':'http://127.0.0.1:8888','https':'http://127.0.0.1:8888' },headers={'content-type': 'application/json', 'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)'}, retry = 2, redir=True):
		#useragent=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1', u'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2', u'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0', u'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00']
		self._timeout = timeout
		self._proxies = proxies
		self._headers = headers
		self._url = url
		self._active_redir = redir
		self._content = None
		self._status_code = None
		self._redirect = None
		self._retries = retry
		self._statusmsg = None

	def fetch(self):
		requests.adapters.DEFAULT_RETRIES = self._retries
		
		if urlparse(self._url).scheme == "https":
			try:
				doc = urllib.urlopen(self._url)
			except Exception, e:
				self._statusmsg = e
				self.__status_code = 418
			self._content = doc.read()
			doc.close()
			self._status_code = 200
			self._redirect = ''
			'''OLD VERSION
			r = requests.get(self._url,cert=None, verify=False, headers=self._headers, 
							allow_redirects=self._active_redir,
							timeout=self._timeout)
			
			'''
				
			print r.headers['status']
		else:
			r = requests.get(self._url,headers=self._headers, allow_redirects=self._active_redir,timeout=self._timeout, proxies=self._proxies)
		
			self._content = r.text
			self._status_code = r.status_code
			self._redirect = r.history
		#~ except requests.exceptions.ConnectionError, e:
			#~ self._status_code = 404
			#~ self._status_msg = e
		return self
		
	def check(self):
		'''COMPLETE MSG OF ERROR'''
		if self._status_code in range(310,499):
			self._status = False
			self._statusmsg = "Page not Found"
			return self
			
		elif len(self._redirect) > 0: 
			self._status = redir
			self._statusmsg = "Redirections are put to %s and Page has mooved" %redir
			return self
			
		elif self._status_code in range(500,520):
			self._status = False
			self._statusmsg = "Server is down, buddy!"	
		
		elif self._status_code in range (200,226):
			self._status = True
			return self
		else:
			self._status = False
			return self

class Page(Connexion):
	'''simple function to dispatch treatement according to the type of Ressources'''
	def __init__(self, url):
		Connexion.__init__(self, url)
		self._values = {}

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
		mini dispatcher for different extracting method using getattr
		'''		
		self.get_type()
		if self._type != None:
			self.fetch()
			self.check()
			try:
				self._values['type'] = self._type
				self._values['url'] = self._url
				if self._status is not False:
					getattr(sys.modules[__name__],self._type)(self)
				else:
					self._values['data'] = [{"status": self._status_code}, {'msg': self._statusmsg}]			
			except AttributeError:
				print "Extractor not implemented for %s" %self._type 
		else:
			print "Type is not defined"
		return self

if __name__ == '__main__':
		#~ msg = Page()
		#~ msg.dispatch()
		#~ print msg._values
		read_url("report.csv")
