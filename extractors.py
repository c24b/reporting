#!/usr/bin/env python
# -*- coding: utf-8 -*-

#parsing
from bs4 import BeautifulSoup as bs
import re

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
	img_details = bs(self._content).findAll("div", {"id":re.compile('^detailPhoto.*?$')})
	#je mets à la ligne parce qu'on me dit que c'est illisible
	self._values['name'] = "instagram"
	self._values['stats'] = dict((y.get_text(), int(x.get_text())) for x, y in user_stats_list)
	self._values["details"] =[{"img":{
								'type': 'img',
								'url':n.find('img')['src'],
								'stats':dict((img.get('class')[0], txt2int(img.get_text())) for img in n.findAll('span'))
								}
								}
								for n in img_details
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
	self._values['stats'] = dict((re.sub(" ","", n.strong.nextSibling).lower(), int(re.sub(r"\D","",n.strong.get_text()))) for n in bs(self._content).find('ul', {'class':'stats'}).findAll('li'))
						 
	return self
	

def facebook(self):
	n = bs(self._content).find_all('code')
	if n is not None:
		res = (n[2].string).encode("utf-8")
		like = re.split("class\=\"fsm.fwn.fcg\"\>|·|\<\/div\>\<\/div\>\<\/h2\>", res)
		self._values['stats'] = {'likes' : int(re.sub(r"\D","", like[2])),'talking': int(re.sub(r"\D","", like[3]))}
		return self
