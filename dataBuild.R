# Load workspace
source('/Users/janus829/Desktop/Research/BITsData/setup.R')

# Replacing BLEU with Belgium (Belgium-Luxem sign BITs under BLEU)
bit$partner=char(bit$partner)
bit$partner[bit$partner=='BLEU (Belgium-Luxembourg Economic Union)']='Belgium'

# Clean country names in BITData
bit=addIDs(bit, panel, c('sender','partner'), TRUE)

# Pull out day, month, year into separate columns
vars=c('sign','ratif','term')
for(ii in vars){
	bit=cbind(bit, dBrk(bit[,paste0(ii,'Date')],  '/', ii)) }

## Set up country-year dataset
# Extending panel to 2014 and back to 1959
dataPanel=addYrPanel(bit, 'signYear', panel[,1:6])

# Accounting for cntry-yrs not in panel but noted
# as having signed a BIT in a given year
dataPanelMiss=addMissPanel(bit, dataPanel)

# Add BIT signing, ratification, and termination data
bitPanel=dataPanelMiss
vars=paste(c('sign','ratif','term'),'Year',sep='')
for(ii in 1:length(vars)){
	bitPanel=cYrBld(bit,'cSender','cPartner',vars[ii],
		paste0(substr(vars[ii],0,1),'bit'),bitPanel,'cname','year') }

# Add cumulative sum of sign and ratif vars
vars=c('sbit','rbit','tbit')
vars=c(vars,paste0(vars,'NoDupl'))
for(var in vars){bitPanel=csumPnl(bitPanel,'cname','year',var)}

## Set up matrix format for network analysis
# Add Luxembourg as a partner to BIT
bitM=bit; luxemData=bitM[bitM$partner=='Belgium',]
luxemData$partner='Luxembourg'; luxemData$cPartner='LUXEMBOURG'
bitM=rbind(bitM, luxemData)

# Convert to network format
signNet=ntBld(dataPanel, bitM, 'signYear', termCheck=TRUE)
ratifNet=ntBld(dataPanel, bitM, 'ratifYear', termCheck=TRUE)

## Save
save(bit, bitPanel, signNet, ratifNet, file='bit.rda')