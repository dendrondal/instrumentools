# Grad School Tools
This is a collection of scripts that help with various I/O and graphing tasks that were common to me in my PhD work. All of these use only libraries installed via the standard Anaconda distribution as of 5.3.0. Untested on windows, but should work in the terminal available through Anaconda Navigator. 

## Installation	
First things first, you need to make sure you have modern python on your machine. If you're a Mac or Linux user, this is as easy as opening a terminal and typing ```python --version```. With Windows machines, there are extra steps. You can either use the [bash terminal in Windows](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) or the [Anaconda terminal](https://docs.anaconda.com/anaconda/navigator/getting-started/#navigator-starting-navigator). Since all of the software is usable via the command line, it's most easily available using pipx:
```python
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install instrumentools
```
From there, pick the tool you want to run, and use ```pipx run TOOL```

[Thermal Analysis (TGA/DSC)](https://github.com/dendrondal/grad_school_tools/tree/master/thermal_analysis)
[CAC Analysis by Fluorometry/UV-Vis](https://github.com/dendrondal/grad_school_tools/tree/master/cac)

## TEM
Utility that renames all TEM files (.tiff) in folder based on metadata present within the image. Useful for sorting images by material. Has only been tested for images output by a JEOL 1230 instrument, may require tweaking for others.
