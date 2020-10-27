# Instrumentools
This is a collection of scripts that help with various I/O and graphing tasks that are common in supramolecular chemistry workflows. All of these use only libraries installed via the standard Anaconda distribution as of 5.3.0. Untested on windows, but should work in the terminal available through Anaconda Navigator or WSL. 

## Installation	
First things first, you need to make sure you have modern python on your machine. If you're a Mac or Linux user, this is as easy as opening a terminal and typing `python --version`. With Windows machines, there are extra steps. You can either use the [bash terminal in Windows](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) or the [Anaconda terminal](https://docs.anaconda.com/anaconda/navigator/getting-started/#navigator-starting-navigator). Since all of the software is usable via the command line, it's most easily available using pipx:

```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install instrumentools
```
From there, any time you open a terminal, you can run one of the following commands. If you ever need additional instruction, type `--help` after one of the commands below. All of these are interactive, meaning they'll walk you through the analysis, but you can also pass your commands directly. For example, rather than just runing `tga_analysis`, you can instead run `tga_analysis --path path/to/your/data --title 'Plot Title'`. Which you prefer depends on your level of comfort with the command line.

## cac_analysis
Takes results from Bruker UV-vis critical aggregation concentration (CAC) experiment and outputs them to both a stacked spectra and the CAC graph. Just run this in a terminal and follow the prompts. Contains options for single wavelength (Nile red) and multi-wavelength (Pyrene, DPH) experiments. 

In the Bruker software, after running all of your experiments, go to File > Export Data, which will allow you to output an Excel sheet with a column for each experiment. For Horiba instrumentation, you can run File > Export > Text/ASCII, and export a .csv file.

## tga_analysis & dsc_analysis 
This allows for plotting of DSC and TGA produced by TA Universal Analysis and MUSE software, respectively. Both allow multiple csv/xls files to be combined into a single plot with a uniform format. This is also sized to where it will fit perfectly into a single column, allowing easy insertion into RSC/ACS templates. 

To use this:

	1. Create a directory for all files you want graphed together on your computer.
	2. Go to File > Export and export either a .csv for Universal Analysis or File > Output to Excel for MUSE.
	3. Once all spectra are exported in proper format, transfer them via flash drive/hard drive to the newly created folder.
	4. Point this script there and run it according to the documentation.

### Naming formalism
This script assumes that you name your files according to WRG standards. That is, your DSC filenames are of the format INITIALS_DATE_FILENAME-DETAILS.txt. The FILENAME-DETAILS is what will show up in the plot legend.

## tem_analysis
Takes a folder of TEM images (preferably in dm3 or dm4 format) and calculates aggregate statistics for particle sizes. Creates a plot and a .csv for
manual/custom plotting, if desired. Automatically detects and sizes
particles, and outputs a visualization like the following after each detection so that you can determine whether the prediction is accurate:

![Example program output](https://github.com/dendrondal/instrumentools/blob/master/Media/12_blobs.png)

If your data is not in dm3 or dm4 format, you will need to manually enter the scaling factor, in nm/pixel. This can be done by opening the image in ImageJ or similar and using the meaurement tool to measure the scale bar. This will give you the ratio, which should be applicable for all images at this scale. For example, a 100nm scale bar has a ratio of 0.204 nm/pixel. 
