#Grad School Tools#

This is a collection of scripts that help with various I/O and graphing tasks that were common to me in my PhD work. All of these use only libraries installed via the standard Anaconda distribution as of 5.3.0. Untested on windows, but should work in the terminal available through Anaconda Navigator.

**thermal_analysis.py** This allows for plotting of DSC and TGA produced by TA Universal Analysis and MUSE software, respectively. Both allow multiple csv/xls files to be combined into a single plot with a uniform format. This is also sized to where it will fit perfectly into a single column, allowing easy insertion into RSC/ACS templates. 

To use this:

	1. Create a directory for all files you want graphed together on your computer.
	2. Go to File > Export and export either a .csv for Universal Analysis or File > Output to Excel for MUSE.
	3. Once all spectra are exported in proper format, transfer them via flash drive/hard drive to the newly created folder.
	4. Point this script there and run it according to the documentation.

**UV-vis_cac.py** Takes results from Bruker UV-vis critical aggregation concentration (CAC) experiment and outputs them to both a stacked spectra and the CAC graph. Just run this in a terminal and follow the prompts. Contains options for single wavelength (Nile red) and multi-wavelength (Pyrene, DPH) experiments. In the Bruker software, after running all of your experiments, go to File > Export Data, which will allow you to output an Excel sheet with a column for each experiment.

**tem_ocr.py** Utility that renames all TEM files (.tiff) in folder based on metadata present within the image. Useful for sorting images by material. Has only been tested for images output by a JEOL 1230 instrument, may require tweaking for others.
