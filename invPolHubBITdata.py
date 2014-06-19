# Helpers
import os

# Choose directory
os.chdir('/Users/janus829/Desktop/Research/BITsData')

# My helper functions
from invPolHubHelpers import *

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
bitData=[] # List of country-treaty data
dwnldTexts=[] # list of texts that have been downloaded

# Run through each link to gather information
for sender in range(0,len(subAddress)):	

	# Control for downed web pages
	try:
		treatyData=treatyScrape(sender, subAddress, cntries, base, True, dwnldTexts)
		bitData.append(treatyData[0]); dwnldTexts.append(treatyData[1])
		moveOn(sender, cntries, 5)

	except urllib2.HTTPError, e:
		print '\n '+  cntries[sender] + ' link not working \n'	

# Write to csv
keys=['sender','partner','signDate','ratifDate','status','termDate','termType','treatyLang']
f=open('BITsData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(bitData)  )