# Choose to download BIT treaty texts
downloadTreaty=True

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
	return bsoup(urllib2.urlopen(x).read())

def cleanStrSoup(x, a, b, adj=None):
	if adj is None: 
		adj=len(a)
	return x[x.find(a)+adj:x.find(b)]

def termInfo(x, tData):
	text=[info for info in x if tData in info][0]
	text=cleanStrSoup(text, '<div class="data">\r\n', '</div>\n</div>')
	return text.replace('\r\n','').strip()

def downloadText(link, dir, filename, sleep):
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
	values=[]
	for i in range(0,len(x)):
		slice=x[i]
		for j in range(0,len(slice)):
			values.append(slice[j])
	return values

# Choose directory
os.chdir('/Users/janus829/Desktop/Research/BITsData')

# Load in parsable version of base webpage from UNCTAD's Investment Policy Hub
address = 'http://investmentpolicyhub.unctad.org/IIA/IiasByCountry#iiaInnerMenu'
soup = openSoup(address)

# Find links to specific countries
strLinks=[]
for i in soup.findAll('span', {'class':'cell-info'}):
	if 'href' in str(i):
		strLinks.append(str(i))

# Create new links to look up and set up helpful labels
base='http://investmentpolicyhub.unctad.org'
subAddress = []
cntries=[]
for i in strLinks:
	subAddress.append(base + cleanStrSoup(i,'a href="','#iiaInnerMenu">'))
	cntries.append(cleanStrSoup(i,'#iiaInnerMenu">','</a></span>'))

# Set up lists for data to be extracted
bitData=[] # Contains all data from UNCTAD

# Run through each link to gather information
for sender in range(0,len(subAddress)):	

	# Control for downed web pages
	try:

		soup=openSoup(subAddress[sender])
		dirtySoup=[soup.findAll('td', {'data-position':str(x)}) for x in range(1,6)]

		treatyData=[]
		for treaty in range(0,len(dirtySoup[0])):

			strSoup=[]
			for broth in dirtySoup:
				strSoup.append(str(broth[treaty]))

			# Find partner, sign/ratif date, and status of treaty
			partner = re.sub('<[^>]+>', ' ', strSoup[0]).strip()
			signDate = cleanStrSoup(strSoup[2], 'fo">', '</span></td>')
			ratifDate = cleanStrSoup(strSoup[3], 'fo">', '</span></td>')
			inForce = cleanStrSoup(strSoup[1], 'fo">', '</span></td>')

			# If status is terminated find date and reason
			termDate=''; termType=''
			if inForce=='Terminated':
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
					tName=cntries[sender]+'_'+partner+signDate[len(signDate)-4:len(signDate)]+'_'+tLang
					if downloadTreaty:
						downloadText(link=tLink, dir='TreatyTexts', filename=tName, sleep=5)
			treatyLang=', '.join(treatyLang)

			# Story data for individual treaty in dictionary
			treatyDict={ 'sender':cntries[sender],
						'partner':partner, 'signDate':signDate, 'ratifDate':ratifDate,
						'inForce':inForce, 'termDate':termDate, 'termType':termType,
						'treatyLang':treatyLang }
			
			# Store all treaties for country in a list
			treatyData.append(treatyDict)

		# Store data for all countries in alist
		bitData.append(treatyData)
		print 'Data for ' + cntries[sender] + ' collected \n'
		time.sleep(5) # Be nice to UNCTAD servers


	except urllib2.HTTPError, e:
		print '\n '+  cntries[sender] + ' link not working \n'	

# Write to csv
keys=['sender','partner','signDate','ratifDate','inForce','termDate','termType','treatyLang']
f=open('BITsData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(bitData)  )