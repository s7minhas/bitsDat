Process for Downloading and Storing BITs Data
===

Download
---

* First we download PDFs using the Download_PDFs.py script, this is located in the Country_BITs folder

	* Check to make sure base URL is current

	* Code downloads PDFs for a set of manually defined 177 countries

Convert PDFs to txt -> Excel
---

* Next we convert each of the PDFs into a tag file using the convert_pdfs.py and Convert_PDFs_toTags.py scripts. These are both located in the main folder. The convert_pdfs.py script feeds into the Convert_PDFs_toTags.py script, it basically uses the function created in convert_pdfs.py to loop through all of downloaded PDFs and generate text versions of the file.

* Then we run the Cleaning_Output_toCSV.py script which is located in the Country_BITs folder. This script loops through all of the text files, cleans them up, and puts the data for each country into a separate CSV file

ToDos
---

* Create simple bash script to do all this