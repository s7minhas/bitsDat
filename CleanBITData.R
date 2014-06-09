# Cleaning BIT data

####################################################################################
# Setting up workspace
rm(list=ls())
setwd('~/Desktop/Research/BITsData')
load('panel.rda')

# Libraries
require(zoo)
require(lubridate)
require(countrycode)

# Helpful functions
num=function(x){as.numeric(as.character(x))}
char=function(x){as.character(x)}

# Pulling in BIT data
setwd('~/Desktop/Research/BITsData/PDF Parser/Country_BITs_UNCTAD')
bits = read.csv('pulls_from_UNCTAD_ALL.csv')
####################################################################################

####################################################################################
# Cleaning Dates

# Convert dates from character format
bits$Sdate=as.Date(char(bits[,3]), format='%d-%b-%y')
bits$Syear=num(year(bits$Sdate))

bits$Rdate=as.Date(char(bits[,4]), format='%d-%b-%y')
bits$Ryear=year(bits$Rdate)

# Correct mistake in as.Date
bits[bits$Syear>2020,'Sdate']=bits[bits$Syear>2020,'Sdate']-365.242*100
bits$Syear[bits$Syear>2020]=bits$Syear[bits$Syear>2020]-100

bits[which(bits$Ryear>2020),'Rdate']=bits[which(bits$Ryear>2020),'Rdate']-365.242*100
bits$Ryear[which(bits$Ryear>2020)]=bits$Ryear[which(bits$Ryear>2020)]-100
####################################################################################

####################################################################################
# Cleaning Country Labels

# Cleaning country names
bits$Reporter=char(bits$Reporter)
bits$Reporter[bits$Reporter=="Democratic People's Republic of Korea"]='North Korea'
bits$Reporter[bits$Reporter=="Congo, DR"]='Congo, Democratic Republic'
bits$Rcntry=countrycode(bits$Reporter, 'country.name', 'country.name')
bits$Rcname=panel$cname[match(bits$Rcntry, panel$cname)] # no codes for macau or hong kong
bits$Rccode=panel$ccode[match(bits$Rcname, panel$cname)]

bits$Partner=char(bits$Partner)
bits$Partner[bits$Partner=="Democratic People's Republic of Korea"]='North Korea'
bits$Partner[bits$Partner=="Congo, DR"]='Congo, Democratic Republic'
bits$Partner[bits$Partner=="São Tomé and Principe"]='Sao Tome and Principe'
bits$Partner[bits$Partner=="and Luxembourg Albania"]='Albania'
bits$Pcntry=countrycode(bits$Partner, 'country.name', 'country.name')
bits$Pcname=panel$cname[match(bits$Pcntry, panel$cname)] # no codes for macau, hong kong, palestine
bits$Pccode=panel$ccode[match(bits$Pcname, panel$cname)]
####################################################################################

# ####################################################################################
# # Save dataset
# save(bits, file='bits.rda')
# ####################################################################################

####################################################################################
# Creating monadic data frame

bits$sbits = 1
bits$rbits = ifelse(is.na(bits$Ryear), 0, 1)
####################################################################################