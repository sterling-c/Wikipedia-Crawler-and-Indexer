from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

#Functions
def get_page_content(url):
	try:
		html_response_text = urlopen(url).read()
		page_content = html_response_text.decode('utf-8')
		return page_content
	except Exception as e:
		return None

def clean_title(title):
	invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
	for c in invalid_characters:
		title = title.replace(c, '')
	return title

def get_urls(soup):
	links = soup.find_all('a')
	urls=[]
	for link in links:
		urls.append(link.get('href'))
	return urls

def is_url_valid(url):
	if url is None:
		return False
	if re.search('#', url):
		return False
	match = re.search('^/wiki/', url)
	if match:
		return True
	else:
		return False

def reformat_url(url):
	match=re.search('^/wiki/', url)
	if match:
		return "https://en.wikipedia.org" + url
	else:
		return url 

def save(text, path):
	f = open(path, 'a+', encoding = 'utf-8', errors = 'ignore')
	f.write(text)
	f.write("\n")
	f.close()



#Procedure Focused Crawler
def FocusedCrawler(seedUrls, relatedTerms):
	urlList = []
	visitedList= []
	pageCounter = 0
	savedList = []
	crawlCount = 0

	try:
		_create_unverified_http_context = ssl._create_unverified_context
	except AttributeError:
		pass
	else:
		ssl._create_default_https_context = _create_unverified_http_context

	for url in seedUrls:
		url = reformat_url(url)
		urlList.append(url)
		visitedList.append(url)
	while(len(urlList)>0):
		url = urlList.pop(0)
		crawlCount += 1
		url = reformat_url(url)
		pageContent = get_page_content(url)
		if pageContent is None:
			continue
		termCounter = 0
		soup = BeautifulSoup(pageContent, 'html.parser')
		page_text = soup.get_text()
		for term in relatedTerms:
			if(re.search(term, page_text, re.I)):
				termCounter = termCounter + 1
				if (termCounter >= 2):
					title = soup.title.string
					title = clean_title(title)
					save("Title: " + title + "\n"  + "url: " + url + " term count: " + str(termCounter), "../Output/saved_urls.txt")
					savedList.append(url)
					pageCounter = pageCounter + 1
					print("page: " + str(pageCounter) + " term count: " + str(termCounter) + " url: " + url)
					break
		if(pageCounter>=500):
			break
		outGoingURLs = get_urls(soup)
		for outGoingURL in outGoingURLs:
			if(is_url_valid(outGoingURL) and outGoingURL not in visitedList):
				urlList.append(outGoingURL)
				visitedList.append(outGoingURL)
	i=1
	f = open("../Output/crawled_urls.txt","a")
	f.write("Total pages crawled: " + str(crawlCount) + "\n")
	for url in savedList:
		f.write(str(i) + ': ' + url)
		f.write("\n")
		i += 1
	f.close()




seedUrls = ["https://en.wikipedia.org/wiki/Sustainable_energy", "https://en.wikipedia.org/wiki/Alternative_energy"]
relevantTerms = ["alternative energy", "solar", "wind", "renewable", "sustanaible", "carbon", "nuclear", "envirorment", "pollution", "biomass"]
FocusedCrawler(seedUrls, relevantTerms)
