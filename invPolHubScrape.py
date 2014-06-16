import time
import urllib2
import os
from BeautifulSoup import BeautifulSoup as bsoup


address = 'http://investmentpolicyhub.unctad.org/IIA/IiasByCountry#iiaInnerMenu'
webpage = urllib2.urlopen(address)
soup = bsoup(webpage.read())

strLinks=[]
for i in soup.findAll('span', {'class':'cell-info'}):
	if 'href' in str(i):
		strLinks.append(str(i))

links=[]
num=[]
cntries=[]
for i in strLinks:
	link=i[i.find('a href="')+8:i.find('#iiaInnerMenu">')]
	links.append(link)
	if link.find('Bits/')+5 == len(link)-1:
		num.append( link[len(link)-1]  )
	else:
		num.append(link[(link.find('Bits/')+5):(len(link))])
	cntries.append(i[i.find('#iiaInnerMenu">')+15:i.find('</a></span>')])

base='http://investmentpolicyhub.unctad.org'
subAddress = []
for i in links:
	subAddress.append(base + i)

senders=[]
partners=[]
signDates=[]
ratifDates=[]
# treatyText=[]

# for sender in range(0,len(subAddress)):
for sender in range(0,5):	

	webpage = urllib2.urlopen(subAddress[sender])
	soup=bsoup(webpage.read())

	pDirty=soup.findAll('td', {'data-position':'1'})
	sDirty=soup.findAll('td', {'data-position':'3'})
	rDirty=soup.findAll('td', {'data-position':'4'})
	# tDirty=soup.findAll('td', {'data-position':'5'})

	j_partner=[]
	j_signDate=[]
	j_ratifDate=[]
	# j_treaty=[]

	for j in range(0,len(pDirty)):

		p=str(pDirty[j]	)
		partner=cntries[[i for i, x in enumerate(cntries) if x in p][0]]
		j_partner.append(partner)

		si=str(sDirty[j])
		signDate=si[si.find('fo">')+4:si.find('</span></td>')]
		j_signDate.append(signDate)

		ri=str(rDirty[j])
		ratifDate=ri[ri.find('fo">')+4:ri.find('</span></td>')]
		j_ratifDate.append(ratifDate)

		# tr=str(tDirty[j])
		# if 'href' in tr:
		# 	treaty=tr[tr.find('ref="')+5:tr.find(' target="')]
		# else:
		# 	treaty='No treaty text'
		# j_treaty.append(treaty)



	# Store data
	senders.append( [cntries[sender]]*len(pDirty) )
	partners.append(j_partner)
	signDates.append(j_signDate)
	ratifDates.append(j_ratifDate)
	# treatyText.append()


	time.sleep(5)