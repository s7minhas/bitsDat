# Setup
setwd('/Users/janus829/Desktop/Research/BITsData')
load('panel.rda')
bit=read.csv('BITsData.csv')

# Libraries
require(countrycode)
require(doBy)

# Helpful functions
cname=function(x){countrycode(x,'country.name','country.name')}
char=function(x){as.character(x)}
num=function(x){as.numeric(as.character(x))}
substrRight=function(x, n){substr(x, nchar(x)-n+1, nchar(x))}

# Add IDs and conduct error check
addIDs=function(data, panel, ids, errorCheck=F){
	for(ii in 1:length(ids)){
		
		# Add cntry names
		nid=paste0('c',toupper(substr(ids[ii],0,1)), 
			substr(ids[ii],2,nchar(ids[ii])))
		data=cbind(data, cname(data[,ids[ii]]))
		colnames(data)[ncol(data)]=nid

		# Add ccode
		nidN=paste0('ccode',toupper(substr(ids[ii],0,1)))
		data=cbind(data, panel[,'ccode']
			[ match(data[,nid], panel[,'cname']) ] )
		colnames(data)[ncol(data)]=nidN

		if(errorCheck){
			# Check for NAs
			noMatch=data[is.na(data[,nidN]),]
			ifErrorPrint(noMatch, nidN, ids[ii])
		}
	}
	data		
}

ifErrorPrint=function(check, nvar, var){
	if(nrow(check)!=0){
		cat(paste0('Following countries do not have ', nvar, ' codes\n'))
		print(check[,c(var, nvar)]); cat('\n')
	}
}

# Breaks dates into day, month, and year
dBrk=function(date, split, prefix){
	brokenDates=matrix(NA, nrow=length(date), ncol=3)
	colnames(brokenDates)=paste0(prefix,c('Day','Month','Year'))
	for(ii in 1:length(date)){
		breaks=strsplit(char(date)[ii], split)[[1]]
		if(length(breaks)!=0){
			if(length(breaks)==2){ brokenDates[ii,2:3]=num(breaks) }
			if(length(breaks)==3){ brokenDates[ii,]=num(breaks) }
			if(length(breaks)>3){ 'more than three date items'  }
		}
	}
	brokenDates
}

# Add missing years to panel
addYrPanel=function(data, dyear, frame){
	toAdd=setdiff(unique(data[,dyear]), unique(frame$year))

	# Add years
	if(length(toAdd)!=0){
		cat(paste0('Adding data for following years: '), toAdd, '\n')
		for(ii in 1:length(toAdd)){
			# Determine position of closest year
			clYr=frame$year[which.min(abs(frame$year-toAdd[ii]))]
			sliceAdd=frame[frame$year==clYr,]
			sliceAdd$year=toAdd[ii]
			frame=rbind(frame, sliceAdd)
		}
		frame
	}
}

# Check for discrepancies between BIT signings
# and year country shows up in panel
addMissPanel=function(bitData, data){

	# Perform check of what's missing
	miss=setdiff( paste0(bitData$cSender, bitData$signYear), 
		paste0(data$cname, data$year) )

	# Convert to matrix
	missCntries=matrix(NA, nrow=length(miss), ncol=2)
	for(ii in 1:length(miss)){
		missCntries[ii,1]=substr(miss[ii], 0, nchar(miss[ii])-4)
		missCntries[ii,2]=substrRight(miss[ii], 4)
	}

	# Check which don't exist in panel at all
	totMiss=setdiff( unique(missCntries[,1]), unique(data$cname) )

	# Drop countries that don't exist at all
	# Leads to exclusion of Hong Kong, Macao, and Palestine
	missCntries=missCntries[which(!missCntries[,1] %in% totMiss),]

	# Add countries to panel
	for(ii in 1:nrow(missCntries)){
		slice=data[data$cname==missCntries[ii,1],][1,]
		slice$year=missCntries[ii,2]	
		data=rbind(slice, data)
	}
	cat('The following country-years were added:\n')
	print(missCntries); cat('\n')
	data
}

# Builds country-year dataset
cYrBld=function(data, id, idP, var, nvar, cyData, cntry, year){
	if( length( setdiff(nvar, colnames(cyData)) )>0 ){	
		# Subset relevant info from event data
		slice=data[,c(id, idP, var)]
		slice=na.omit(slice)
		toSumm=data.frame(cbind(char(slice[,1]),slice[,3],1))
		colnames(toSumm)=c(id,var,nvar)
		toSumm[,var]=num(toSumm[,var]); toSumm[,nvar]=num(toSumm[,nvar])

		# Remove duplicate partner countries (keep early version)
		sliceD=cbind(slice,sp=paste(slice[,id],slice[,idP],sep='_'))
		fm=formula(paste0(var,'~ sp'))
		minYr=summaryBy(fm, data=sliceD, FUN=min, keep.names=TRUE)
		cpairs=matrix(
			unlist( strsplit( char( minYr[,'sp'] ), '_' ) ),
			ncol=2, byrow=TRUE )
		toSummD=data.frame(cbind(cpairs[,1], minYr[,var], 1))
		colnames(toSummD)=c(id,var,nvar)
		toSummD[,var]=num(toSummD[,var]); toSummD[,nvar]=num(toSummD[,nvar])
		
		# Calculate number of occurences by year
		fm=formula(paste0(nvar,'~', id, '+', var))
		yrSumm=summaryBy(fm, data=toSumm, FUN=sum, keep.names=TRUE)
		yrSummD=summaryBy(fm, data=toSummD, FUN=sum, keep.names=TRUE)
		colnames(yrSummD)[3]=paste0(nvar,'NoDupl')

		# Merge in to dataset
		cyData$mVar=paste0(cyData[,cntry], cyData[,year])
		yrSumm$mVar=paste0(yrSumm[,id], yrSumm[,var])
		tmp=merge(cyData, yrSumm[,3:4], by='mVar', all.x=T)
		yrSummD$mVar=paste0(yrSummD[,id], yrSummD[,var])
		tmp=merge(tmp, yrSummD[,3:4], by='mVar', all.x=T)		
		
		# Clean up merged file and remove merge variable
		tmp[is.na(tmp[,nvar]),nvar]=0
		tmp[is.na(tmp[,paste0(nvar,'NoDupl')]),paste0(nvar,'NoDupl')]=0		
		tmp[,2:ncol(tmp)]
		} else { cat(paste0(nvar, ' already in dataset\n')) } 
}

# Rolling sum of BITs
csumPnl=function(data,cntry,year,var){
	data=cbind(data, NA)
	colnames(data)[ncol(data)]=paste0(var, 'C')
	data=data[order(data[,cntry],data[,year]),]
	cntries=unique(data[,cntry])
	for(ctry in cntries){
		data[which(data[,cntry]==ctry),paste0(var, 'C')] = 
			cumsum(data[which(data[,cntry]==ctry),var])
	}
	data
}

# Builds list of adjacency matrices
ntBld=function(frame, data, nvar, termCheck=TRUE){
	years=sort(num(unique(frame$year)))
	netFrames=lapply(years, function(x) FUN=frame[frame$year==x,'ccode'])

	matList=list()
	for(ii in 1:length(years)){
		slice=data[which(years[ii]>=data[,nvar]),]  
		
		ctrs=netFrames[[ii]]
		mat=matrix(0, nrow=length(ctrs), ncol=length(ctrs), 
			dimnames=list(ctrs, ctrs))

		for(jj in 1:nrow(slice)){
			sndr=NULL; rcvr=NULL
			sndr=slice[jj,'ccodeS']; sndr=as.character(sndr[!is.na(sndr)])
			rcvr=slice[jj,'ccodeP']; rcvr=as.character(rcvr)
			if( length(intersect(c(sndr, rcvr),rownames(mat)))==2 ){
				if(!termCheck){
					mat[sndr, rcvr]=1 
				} else {
					if(is.na( slice[jj,'termYear'] )){
						slice[jj,'termYear']=3000 }
					if( slice[jj, 'termYear']>years[ii] ){
						mat[sndr, rcvr]=1 }
					}
			}
		}
		matList[[ii]]=mat
		cat(paste0(years[ii],' matrix made...'),'\n')
	}
	names(matList)=years
	matList
}