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

# for i in range(0,len(subAddress)):

i=0

webpage = urllib2.urlopen(subAddress[i])
soup=bsoup(webpage.read())

pDirty=soup.findAll('td', {'data-position':'1'})
sDirty=soup.findAll('td', {'data-position':'3'})
rDirty=soup.findAll('td', {'data-position':'4'})
tDirty=soup.findAll('td', {'data-position':'5'})

# for j in range(0,len(partners)):

j=0

p=str(pDirty[j]	)
pLink='/treaty/'+str(j+1)
partner=p[p.find(pLink)+len(pLink)+2:p.find('</a></span></td>')]

si=str(sDirty[j])
signDate=si[si.find('fo">')+4:si.find('</span></td>')]

ri=str(rDirty[j])
ratifDate=ri[ri.find('fo">')+4:ri.find('</span></td>')]



