# Helpers
import time
import urllib2
import os
import re
from BeautifulSoup import BeautifulSoup as bsoup
import csv
import pattern
from pattern.web import URL

# Helper functions
def openSoup(x):
	"""Opens URL and create soup"""
	return bsoup(urllib2.urlopen(x).read())

def cleanStrSoup(x, a, b, adj=None):
	"""Returns the text between strings a and b"""
	if adj is None: 
		adj=len(a)
	return x[x.find(a)+adj:x.find(b)]

def termInfo(x, tData):
	"""Removes data from HTML string associated with tData"""
	text=[info for info in x if tData in info][0]
	text=cleanStrSoup(text, '<div class="data">\r\n', '</div>\n</div>')
	return text.replace('\r\n','').strip()

def downloadText(link, dir, filename, sleep):
	"""Downloads PDF file at given link and places in dir"""
	cur=os.getcwd()
	if not os.path.exists(dir):
		os.makedirs(dir)
	os.chdir(dir)
	Ddir=os.getcwd()
	files=[f for f in os.listdir(Ddir) if os.path.isfile(os.path.join(Ddir, f)) ]
	if filename+'.pdf' not in files: 
		url=URL(link)
		try:
			f=open(filename+'.pdf','wb')
			f.write(url.download(cached=False))
			f.close()
			print filename + ' stored'
			time.sleep(sleep)
		except pattern.web.HTTP500InternalServerError, e:
			print '\n '+ filename + ' link broken' + '\n '
	os.chdir(cur)

def pullout(x):
	"""Pulls out individual dictionary element from a 
	list that contains a list of dictionaries"""
	values=[]
	for i in range(0,len(x)):
		slice=x[i]
		for j in range(0,len(slice)):
			values.append(slice[j])
	return values

def treatyScrape(sender, subAddress, cntries, base, downloadTreaty, dwnldTexts):
	"""Scrapes all treaty data for a particular sender.
	Sender should be a numeric index that gives the position
	of a country in the subAddress or cntries list. subAddress
	is a list of links to individual country pages on UNCTAD.
	Cntries is a list of countries for which data is being
	gathered. Base provides the homepage for investment policy hub. 
	downloadTreaty is a boolean indicating whether or not to download treaties and
	dwnldTexts is a running list of treaties downloaded to avoid dupliactes.
	"""
	soup=openSoup(subAddress[sender])
	dirtySoup=[soup.findAll('td', {'data-position':str(x)}) for x in range(1,6)]

	treatyData=[] # List of treaties for country, treaty info in dict format
	for treaty in range(0,len(dirtySoup[0])):

		strSoup=[]
		for broth in dirtySoup:
			strSoup.append(str(broth[treaty]))

		# Find partner, sign/ratif date, and status of treaty
		partner = re.sub('<[^>]+>', ' ', strSoup[0]).strip()
		
		if cntries[sender]=='Belgium' and partner=='BLEU (Belgium-Luxembourg Economic Union)':
			treatyDict=treatyPgScrape(base, strSoup, partner, cntries, sender, 5)

		else:
			signDate = cleanStrSoup(strSoup[2], 'fo">', '</span></td>')
			ratifDate = cleanStrSoup(strSoup[3], 'fo">', '</span></td>')
			status = cleanStrSoup(strSoup[1], 'fo">', '</span></td>')

			# If status is terminated find date and reason
			termDate=''; termType=''
			if status=='Terminated':
				treatyLink = base + cleanStrSoup(strSoup[0], 'ref="', '">'+partner)
				treatySoup = openSoup(treatyLink)
				stInfo = [str(tI) for tI in treatySoup.findAll('div', {'class':'form-data'})]
				termDate = termInfo(stInfo, 'Date of termination')
				termType = termInfo(stInfo, 'Type of termination')

			# If there is a treaty text, find languages and download
			treatyLang=[]
			if 'Full text' in strSoup[4]:
				text=strSoup[4].split(' | ')
				for t in text:
					tLang=cleanStrSoup(t, '"_blank">', '</a>')
					treatyLang.append(tLang)
					tLink=base+cleanStrSoup(t, 'ref="', '" target="')
					tName=cntries[sender]+'_'+partner+'_'+signDate[len(signDate)-4:len(signDate)]+'_'+tLang
					if downloadTreaty and tLink not in dwnldTexts:
						downloadText(link=tLink, dir='TreatyTexts', filename=tName, sleep=5)
					dwnldTexts.append(tLink)
			treatyLang=', '.join(treatyLang)

			# Story data for individual treaty in dictionary
			treatyDict={ 'sender':cntries[sender],
						'partner':partner, 'signDate':signDate, 'ratifDate':ratifDate,
						'status':status, 'termDate':termDate, 'termType':termType,
						'treatyLang':treatyLang }
		
		# Store all treaties for country in a list
		treatyData.append(treatyDict)

	return [treatyData , dwnldTexts]

def moveOn(sender, cntries, sleep):
	""" Prints message and sleeps for a few seconds  """
	print 'Data for ' + cntries[sender] + ' collected \n'
	time.sleep(sleep) # Be nice to UNCTAD servers

def treatyPgScrape(base, strSoup, partner, cntries, sender, sleep):
	""" Error in the partner entry on the Belgium page on inv policy hub. 
	Error necessitates that I scrape the individual treaty pages. Base is
	simply the base link, strSoup is the string version of the soup from
	the Belgium page.   """
	treatyLink = base + cleanStrSoup(strSoup[0], 'ref="', '">'+partner)
	treatySoup = openSoup(treatyLink)
	stInfo = [str(tI) for tI in treatySoup.findAll('div', {'class':'form-data'})]

	# Info to extract
	ids={'partner':'Parties', 'status':'Status', 'signDate':'Date of signature', 
		'ratifDate':'Date of entry into force', 'treatyLang':'Treaty full text',
		'termDate':'Date of termination', 'termType':'Type of termination'}

	# Extracting info from page into dictionary
	for id in ids.keys(): 
		if id=='partner':
			ids[id]=cleanStrSoup(cleanStrSoup(stInfo[0]+'xxxx', '2. <a', 'xxxx'), 'Menu">', '</a></li>')
		else:
			text=[info for info in stInfo if ids[id] in info]
			if id=='treatyLang':
				langs=[]
				text=str(text).split(' | ')
				for t in text:
					langs.append(cleanStrSoup(t, '"_blank">', '</a>')	)
				ids[id]=', '.join(langs)
			elif len(text) !=0 :
				ids[id]=cleanStrSoup(text[0], 'class="data">\r\n', '\r\n        </div>').strip()
			else:
				ids[id]=''

	# Storing info into new dictionary that matches format of BIT data
	treatyDict={ 'sender':cntries[sender],
						'partner':ids['partner'], 'signDate':ids['signDate'], 'ratifDate':ids['ratifDate'],
						'status':ids['status'], 'termDate':ids['termDate'], 'termType':ids['termType'],
						'treatyLang':ids['treatyLang'] }
	time.sleep(sleep)
	return treatyDict