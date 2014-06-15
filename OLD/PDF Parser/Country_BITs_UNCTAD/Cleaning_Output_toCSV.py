# cleaning txt files
# storing info from text file to csv

# store info in csv

import string
import csv
import os
os.chdir('/users/janus829/desktop/research/BITsData/PDF Parser/Country_BITs_UNCTAD/')

countries = ['bits_zimbabwe.txt','bits_zambia.txt','bits_yemen.txt','bits_vietnam.txt','bits_venezuela.txt','bits_uzbekistan.txt','bits_us.txt','bits_uruguay.txt','bits_ukraine.txt','bits_uk.txt','bits_uganda.txt','bits_uae.txt','bits_turkmenistan.txt','bits_turkey.txt','bits_tunisia.txt','bits_Trinidad and Tobago.txt','bits_tonga.txt','bits_togo.txt','bits_timor.txt','bits_thailand.txt','bits_tanzania.txt','bits_tajikistan.txt','bits_taiwan.txt','bits_syria.txt','bits_switzerland.txt','bits_sweden.txt','bits_swaziland.txt','bits_suriname.txt','bits_sudan.txt','bits_sri_lanka.txt','bits_spain.txt','bits_south_africa.txt','bits_somalia.txt','bits_slovenia.txt','bits_slovakia.txt','bits_singapore.txt','bits_sierra_leone.txt','bits_seychelles.txt','bits_serbia.txt','bits_senegal.txt','bits_saudi_arabia.txt','bits_sao_tome.txt','bits_san_marino.txt','bits_saint_vincent.txt','bits_saint_lucia.txt','bits_rwanda.txt','bits_russia.txt','bits_romania.txt','bits_qatar.txt','bits_portugal.txt','bits_poland.txt','bits_philippines.txt','bits_peru.txt','bits_paraguay.txt','bits_papua_new_guinea.txt','bits_panama.txt','bits_pakistan.txt','bits_oman.txt','bits_norway.txt','bits_nigeria.txt','bits_niger.txt','bits_nicaragua.txt','bits_new_zealand.txt','bits_netherlands.txt','bits_nepal.txt','bits_namibia.txt','bits_myanmar.txt','bits_mozambique.txt','bits_morocco.txt','bits_Montenegro.txt','bits_mongolia.txt','bits_moldova.txt','bits_mexico.txt','bits_mauritius.txt','bits_mauritania.txt','bits_malta.txt','bits_mali.txt','bits_malaysia.txt','bits_malawi.txt','bits_Madagscar.txt','bits_macedonia.txt','bits_Macao.txt','bits_lithuania.txt','bits_libya.txt','bits_liberia.txt','bits_lesotho.txt','bits_lebanon.txt','bits_latvia.txt','bits_lao_pdr.txt','bits_Kyrgyzstan.txt','bits_kuwait.txt','bits_korea_republic.txt','bits_korea_dpr.txt','bits_kenya.txt','bits_kazakhstan.txt','bits_jordan.txt','bits_japan.txt','bits_jamaica.txt','bits_italy.txt','bits_israel.txt','bits_ireland.txt','bits_iraq.txt','bits_Iran.txt','bits_indonesia.txt','bits_india.txt','bits_iceland.txt','bits_hungary.txt','BITs_Honduras.txt','bits_hk_china.txt','bits_haiti.txt','bits_guyana.txt','bits_guinea.txt','bits_guinea_bissau.txt','bits_guatemala.txt','bits_grenada.txt','bits_greece.txt','bits_ghana.txt','bits_germany.txt','bits_georgia.txt','bits_gambia.txt','bits_gabon.txt','bits_france.txt','bits_finland.txt','bits_ethiopia.txt','bits_estonia.txt','bits_eritrea.txt','bits_equatorial_guinea.txt','bits_el_salavador.txt','bits_egypt.txt','bits_ecuador.txt','bits_dominica.txt','bits_Dominica_rep.txt','bits_djibouti.txt','bits_denmark.txt','bits_czech_rep.txt','bits_cyprus.txt','bits_cuba.txt','bits_croatia.txt','bits_Cote_Ivoire.txt','bits_costa_rica.txt','bits_congo.txt','bits_congo_dr.txt','bits_comoros.txt','bits_colombia.txt','bits_china.txt','bits_chile.txt','bits_chad.txt','bits_central_african_rep.txt','bits_cape_verde.txt','bits_canada.txt','bits_cameroon.txt','bits_cambodia.txt','bits_burundi.txt','bits_burkina_faso.txt','bits_bulgaria.txt','bits_Brunei_darussalam.txt','bits_brazil.txt','bits_botswana.txt','bits_bosnia_herz.txt','bits_bolivia.txt','bits_benin.txt','bits_belize.txt','bits_belgium_luxum.txt','bits_belarus.txt','bits_barbados.txt','bits_bangladesh.txt','bits_bahrain.txt','bits_azerbaijan.txt','bits_austria.txt','bits_australia.txt','bits_armenia.txt','bits_argentina.txt','bits_antigua.txt','bits_angola.txt','bits_algeria.txt','bits_albania.txt','bits_afghanistan.txt']
countries2 = ['Zimbabwe','Zambia','Yemen','Viet Nam','Venezuela','Uzbekistan','United States','Uruguay','Ukraine','United Kingdom','Uganda','United Arab Emirates','Turkmenistan','Turkey','Tunisia','Trinidad and Tobago','Tonga','Togo','Timor-Leste','Thailand','Tanzania, UR','Tajikistan','Taiwan Province of China','Syrian Arab Republic','Switzerland','Sweden','Swaziland','Suriname','Sudan','Sri Lanka','Spain','South Africa','Somalia','Slovenia','Slovakia','Singapore','Sierra Leone','Seychelles','Serbia','Senegal','Saudi Arabia','Sao Tome and Principe','San Marino','Saint Vincent and the Grenadines','Saint Lucia','Rwanda','Russian Federation','Romania','Qatar','Portugal','Poland','Philippines','Peru','Paraguay','Papua New Guinea','Panama','Pakistan','Oman','Norway','Nigeria','Niger','Nicaragua','New Zealand','Netherlands','Nepal','Namibia','Myanmar','Mozambique','Morocco','Montenegro','Mongolia','Moldova','Mexico','Mauritius','Mauritania','Malta','Mali','Malaysia','Malawi','Madagascar','Macedonia, TFYR','Macau','Lithuania','Libyan Arab Jamahiriya','Liberia','Lesotho','Lebanon','Latvia',"Lao, PDR",'Kyrgyzstan','Kuwait','Republic of Korea',"Democratic People's Republic of Korea",'Kenya','Kazakhstan','Jordan','Japan','Jamaica','Italy','Israel','Ireland','Iraq','Iran (Islamic Republic of)','Indonesia','India','Iceland','Hungary','Honduras','Hong Kong Special Administrative Region of China','Haiti','Guyana','Guinea','Guinea Bissau','Guatemala','Grenada','Greece','Ghana','Germany','Georgia','Gambia','Gabon','France','Finland','Ethiopia','Estonia','Eritrea','Equatorial Guinea','El Salvador','Egypt','Ecuador','Dominica','Dominican Republic','Djibouti','Denmark','Czech Republic','Cyprus','Cuba','Croatia',"Cote D'ivoire",'Costa Rica','Congo','Congo, DR','Comoros','Colombia','China','Chile','Chad','Central African Republic','Cape Verde','Canada','Cameroon','Cambodia','Burundi','Burkina Faso','Bulgaria','Brunei Darussalam','Brazil','Botswana','Bosnia and Herzegovina','Bolivia','Benin','Belize','Belgium','Belarus','Barbados','Bangladesh','Bahrain','Azerbaijan','Austria','Australia','Armenia','Argentina','Antigua and Barbuda','Angola','Algeria','Albania','Afghanistan']
snums=[]
letters=string.ascii_lowercase
for x in range(1,10): snums.append(str(x))

Reporter = []
Partner = []
Signature = []
Entry_Force = []

for i in range(0, len(countries)):

    # Load in data
    data = str(countries[i])
    sl = open(data).read()

    # Clears everything from text before and after data
    sl2 = sl[sl.find('Date of entry into force ') + 25 : sl.find('  </page>\n')]

    # Clears out the name of the country in the current text file
    sl3 = sl2[sl2.find(countries2[i])+len(countries2[i]): len(sl2)]

    # Adds semicolons to separate each of the columns and observations
    sl4= sl3.replace(';',',').replace(' -', ';-').replace('- ', '-;').replace(' 1', ';1').replace(' 2',';2').replace(' 3',';3').replace(' 4',';4').replace(' 5',';5').replace(' 6',';6').replace(' 7',';7').replace(' 8',';8').replace(' 9',';9').replace(' 0',';0').replace('1 ','1;').replace('2 ','2;').replace('3 ','3;').replace('4 ','4;').replace('5 ','5;').replace('6 ','6;').replace('7 ','7;').replace('8 ','8;').replace('9 ','9;').replace('0 ','0;').replace('> ','>;').replace(' >',';>')

    # Uses the semicolons as an identifier to separate each of the values into a list
    sl5 = sl4.split(';')

    # Further cleaning out unnecessary words
    sl6 = [x for x in sl5 if "bbox" not in x]

    # Removes empty objects in list created by extra spaces in country names
    sl7=[]

    for m in range(0, len(sl6)):
        stripped = sl6[m].strip()
        if stripped != '': sl7.append(stripped)

    # find position of all countries in text
    cPos=[]
    for c in sl7:
        if c[0].lower() in letters: cPos.append(sl7.index(c))

    # find places where countries dont have three pieces of information
    cPosD=[d[1] -d[0] for d in zip(cPos[:-1], cPos[1:])]

    # Add in necessary dashes
    for j in range(0,len(cPos)-1):
        if cPosD[j]!=3: 
            sl7.insert( cPos[j+1],'---')
            cPosD[j]=3
            cPos[j+1:len(cPos)]=[x+1 for x in cPos[j+1:len(cPos)]]

    # Make sure last country entry has a entry in the second column
    if len(sl7) % 3 != 0: sl7.insert(len(sl7), '---')

    # Converts list into dictionary by converting each row of data into one object within dictionary and then the various columns as different elements within the object in the dictionary
    sl8 = [sl7[j:j+3] for j in range(0, len(sl7), 3)]

    # Adding in a column of country identifiers
    reporter = []
    reporter = [countries2[i]]*len(sl8)

    # Creating country specific excel sheets

    filename = 'pulls_from_UNCTAD_' + str(countries[i])[0:len(countries[i])-3] + 'csv'

    with open(filename, 'wb') as f:
        my_writer = csv.DictWriter(f, fieldnames=("Reporter", "Partner","Date of Signature","Date of entry into force"))
        my_writer.writeheader()
        for k in range(0, len(sl8)):
            my_writer.writerow({"Reporter":reporter[k], "Partner":sl8[k][0],"Date of Signature":sl8[k][1], "Date of entry into force":sl8[k][2]})
            Reporter.append(reporter[k])
            Partner.append(sl8[k][0])
            Signature.append(sl8[k][1])
            Entry_Force.append(sl8[k][2])

    # Counter for loop
    print "Just finished creating csv for %s." % countries2[i]

# Creating excel sheet where all data is dumped into one file 

filename = 'pulls_from_UNCTAD_ALL.csv'
with open(filename, 'wb') as f:
  my_writer = csv.DictWriter(f, fieldnames=("Reporter","Partner","Date of Signature","Date of entry into force"))
  my_writer.writeheader()
  for l in range(0, len(Reporter)):
    my_writer.writerow({"Reporter":Reporter[l], "Partner":Partner[l], "Date of Signature":Signature[l], "Date of entry into force":Entry_Force[l]})
