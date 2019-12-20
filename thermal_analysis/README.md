## Thermal Analysis
 This allows for plotting of DSC and TGA produced by TA Universal Analysis and MUSE software, respectively. Both allow multiple csv/xls files to be combined into a single plot with a uniform format. This is also sized to where it will fit perfectly into a single column, allowing easy insertion into RSC/ACS templates. 

To use this:

	1. Create a directory for all files you want graphed together on your computer.
	2. Go to File > Export and export either a .csv for Universal Analysis or File > Output to Excel for MUSE.
	3. Once all spectra are exported in proper format, transfer them via flash drive/hard drive to the newly created folder.
	4. Point this script there and run it according to the documentation.

### Naming formalism
This script assumes that you name your files according to WRG standards. That is, your DSC filenames are of the format INITIALS_DATE_FILENAME-DETAILS.txt. The FILENAME-DETAILS is what will show up in the plot legend.