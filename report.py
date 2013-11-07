#!/usr/bin/env/python
# -*- coding: utf-8 -*-
from send_reportbymail import *
import os, datetime, time
import urllib, re, json
from BeautifulSoup import BeautifulSoup
import smtplib
from jinja2 import Environment, FileSystemLoader

import csv
	
def timer(foo):
	#startTime = time.time()
	foo()
	return time.time()-startTime 

def calc(new, old):
	calcul = (int(new))-old
	if calcul < 0:
		return str(calcul)
	elif calcul == 0:
		return "="
	else:
		return "+"+str(calcul)

def scrape(url):
	try:
		doc = urllib.urlopen(url)
	except Exception, e:
		return e
	html = doc.read()
	doc.close()
	raw = BeautifulSoup(html)
	#print  time.time()-startTime
	return raw

 
def write_values(new_liste, file="stats.csv"):
	THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	os.path.join(THIS_DIR, file)
	with open(file, 'wb') as f:
		reader = csv.writer(f, delimiter=",")
		for row in new_liste:
			reader.writerow(row)

def read_values(file="stats.csv"):
	THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	file = os.path.join(THIS_DIR, file)
	values = []
	with open(file, 'rb') as f:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			values.append(row)
	return values 

def extract_instgr(raw):
	value =  raw.findAll("span", {"class": "chiffre"})
	return value[1].text
	
def extract_youtube(raw):
	video1 =  raw.find("span", {"class": "watch-view-count "}).text
	value = re.sub(ur"[^0-9]","",video1)
	return value
			

def extract_tw(raw):
	res = raw.find('input', {'class':'json-data'})
	data = json.loads(res['value'])
	value = data['profile_user']['followers_count']
	return value


def extract_fb(raw):
	n = raw.findAll('code')
	if n is not None:
		res = (n[2].string).encode("utf-8")
		like = re.split("fcg.>|J\’aime", res)
	
		value = re.sub(ur"[^0-9]","", like[2])
		return value.encode('ascii','replace').decode('ascii')
	else:
		pass

def update_values(method, file):
	archives = read_values(file)
	for n in archives:
		v = method(scrape(n[1]))
		n.append(v)
	write_values(archives, file)
		
def render_values(file):
		name = []
		new_values = []
		diff = []
		archives = read_values(file)
		for n in archives:
			index = len(n)
			name.append(n[0]) 
			new_values.append(n[index-1])
			diff.append(calc(int(n[index-1]), int(n[index-2])))
		return zip(name,new_values, diff)

def print_html_doc(twitter, facebook):
	title ="Bilan veille Hello Bank !"
	now = datetime.datetime.now()
	date = now.strftime("%d Juin %Y %H:%M")
	THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	
	j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
	trim_blocks=True)
	return j2_env.get_template('template.html').render(
	title=title, date=date, twitter=twitter, facebook= facebook, video = video, instagram = instagram)

def send_report(date, message):
	html = msg.encode('utf-8')
	text = 'If this email is not showing correctly ?.....'
	now = datetime.now()
	date = now.strftime("%d %m %Y %H:%M")
	subject = "REPORT", date
	message = createhtmlmail(html, text, subject, 'From XXXX')
	server = smtplib.SMTP("smtp.gmail.com","587")
	# Credentials (if needed)
	username = 'username'
	password = 'passwd'

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail('username', toEmail, message)
	server.quit()
	return 'ok'
    
if __name__ == '__main__':
	update_values(extract_fb, "facebook.csv")
	facebook = render_values("facebook.csv")
	update_values(extract_tw, "twitter.csv")
	twitter = render_values("twitter.csv")
	
	msg = print_html_doc(twitter, facebook)
	title = "Title of Alert"
	send_report(date, msg)
	
