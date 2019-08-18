import nltk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

def get_page_content(url):
	try:
		html_response_text = urlopen(url).read()
		page_content = html_response_text.decode('utf-8')
		return page_content
	except Exception as e:
		return None

def Position_Indexing(file_path):	#This function only takes the file as a parameter because the unique terms are taken later within the function
	try:
		_create_unverified_http_context = ssl._create_unverified_context
	except AttributeError:
		pass
	else:
		ssl._create_default_https_context = _create_unverified_http_context

	indexTable = {}
	terms = []
	docCounter = 0
	inputDone = False

	while(inputDone == False):
		inputTerm = input('Enter "DONE" when you are finished with input. Enter a term to search for: ') 
		#For this program I have the User enter the unique terms. When they are done, they enter the 'DONE' exactly as shown. 
		if(inputTerm == 'DONE'):
			inputDone = True
		else:
			terms.append(inputTerm)
	print(terms)

	with open(file_path, "r") as f:
		fContent = f.read()
		#I saved all of my output from the previous program into a text file, so I have to retrieve all URLs from there.
	docList = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fContent)
	#This isolates the URL information from all other information in the text file.
	for document in docList:
		pos = 0
		docContent = get_page_content(document)
		docCounter += 1
		soup = BeautifulSoup(docContent, 'html.parser')
		doc_text = soup.get_text()
		docTokens = nltk.word_tokenize(doc_text.lower())
		for token in docTokens:
			pos += 1
			if(token not in indexTable):
				indexTable[token] = []
			indexTable[token].append([docCounter, pos])
	output = open('pos_index.txt', 'w', encoding = 'utf-8')
	for term in terms:
		indexCount = 0
		output.write(term + ' => ')
		for index in indexTable:
			if(term == index): 
				for posting in indexTable[index]:
					indexCount += 1
					doc_index = str(posting[0])
					output.write(doc_index)
		output.write('\n' + 'Number of pages indexed: ' + str(indexCount) + '\n')
	f.close()
Position_Indexing("crawled_urls.txt")