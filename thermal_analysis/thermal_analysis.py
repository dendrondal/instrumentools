# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:39:19 2016

@author: jwill
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib import ticker
import re
import glob
import click
from cycler import cycler
from pathlib import Path


def tga_plot(cwd, title, filenames=None):
    """
    Plotting utility for TGA. In order to used, TGA must be exported as .xls
    via the analysis software on the TGA computer.
    ------------
    Parameters
    ------------
    filenames: all of the filenames you want to stack on top of each other,
    in quotes, in square brackets. For examle, if you want to compare 90-30    
    G3-PAMAM-PLLA, enter ['90-L-G3', '70-L-G3', '50-L-G3', '30-L-G3'].
    If filenames is None, automatically plots everything in directory
    
    cwd: file location where excel files are located (for example, if 
    they're in your flash drive folder, enter 'F:/yourname/' in quotes)
    """

    decomposition = []
    
    fig, ax = plt.subplots(figsize=(3.0, 2.5))
    
    if filenames is None:
        filenames = [file for file in Path(cwd).glob("*.txt")]
        
    for name in filenames:
        df = pd.read_excel(f'{cwd}/{name}', 
                           skiprows=20, inplace=True)
        TG_ = [100]
        #converts raw mass measurements into % decomposition
        for j in range(1, len(df['ug'])):
            TG_.append((df['ug'][j] / df['ug'][0])*100)
        df['TG(Percent)'] = TG_
        #list of decomposition temps is made to use in plot labels or output.
        decomposition.append(df.loc[df['TG(Percent)'].apply(lambda x:
                                                            int(x)) == 95, 
                                                            'Cel'].mean())
    
        #Previously used plotting parameters are greyed out. May still be wanted.
        #plt.title(title, family='arial', weight='bold')
        plt.xlabel('Temperature', family='arial', weight='bold', size=10)
        #plt.xticks(np.arange(df['Cel'].min(), df['Cel'].max(),10),
        #           labels=None)
        plt.ylabel('%TG', family='arial', weight='bold', size=10)
        #plt.yticks(np.arange(df['TG(Percent)'].min(), df['TG(Percent)'].max(),1),
        #           labels=None)
        #fig.patch.set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.axis('off')
        plt.plot(df['Cel'], TG_, 
                 label=f'{name[:-4].upper()}',
                 linewidth=2)
        plt.tight_layout()
        plt.legend()
        plt.savefig(os.path.join(cwd, f'{title}.png'), dpi=1440)
        
    return decomposition


def csv_extraction(path, save=False):
    """Takes in .txt file output by TA software and parses into individual 
    cyles. If save boolean is true, saves .csv version of file
    with same name as TA .txt output."""
    with open(path, encoding='utf-16') as f:
        for i, line in enumerate(f):
            if 'OrgFile' in line:
                #Some files are output with different starting lines.
                start = i+1
                break
            else:
                start = 68
                #default starting line for output data
        df = pd.read_csv(path, delim_whitespace=True, skiprows=start, 
                         header=None, encoding='utf-16')

    df.columns = ['time (min)', 'temperature (C)', 'heat flow (mW)', 
                  'heat capacity (mJ/C)', 'N2 flow'] 
    num = 0
    
    def cycle(x):
        nonlocal num
        if x['time (min)'] == -2:
            #for some reason, this denotes a switch between heating/cooling
            num += 1
        return num
    
    df['cycle'] = df.apply(cycle, axis=1)
    if save:
        df.to_csv('{}.csv'.format(path.split('/')[-1]))
        
    return df

def save_multiple_csvs(cwd):
    os.chdir(cwd)
    for file in glob.glob("*.txt"):
        csv_extraction(file, save=True)
    
    
def dsc_plotting(cwd, title, cycle=2, filenames=None, legend=False):
    """Creates stacked plot of all DSC data from multiple .csvs
    ------------
    Parameters
    ------------
    cwd: file location where csv files are located (for example, if 
    they're in your flash drive folder, enter 'F:/yourname/datafolder' in quotes)
    
    title: title of saved .png file
    
    filenames: all of the filenames you want to stack on top of each other,
    in quotes, in square brackets. For examle, if you want to compare 90-30    
    G3-PAMAM-PLLA, enter ['90-L-G3', '70-L-G3', '50-L-G3', '30-L-G3'].
    If filenames is None, automatically plots over all .txt files in cwd.
    
    cyle: cycle number to be plotted. 
    
    legend: whether or not to include legend object with plot.
    
    """

    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    ax.set_prop_cycle(cycler('color', ['y', 'g', 'b', 'r']))
    
    if filenames is None:
        filenames = [file for file in Path(cwd).glob("*.txt")]
    elif type(filenames) is str:
        filenames = list(filenames)
    else:
        raise TypeError('filenames must be list of strings or None.')
        
    for i, name in enumerate(filenames):
        df = csv_extraction(name)
        #Plot formatting goes here
        plt.xlabel('Temperature ($^o$C)', family='arial', weight='bold', size=8)
        plt.ylabel('Heat Flow (mW)', family='arial', weight='bold', size=8)
        minor_locator = ticker.AutoMinorLocator()
        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(4))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='both', which='major', labelsize=6)
        #custom y-axis, if needed:
        #ax.set_ylim([-1, -0.6])
        plt.tight_layout()
        if legend:
            plt.legend(prop={'size':6}, frameon=False)

        df = normalize(df)
        #This operation introduces offset between the graphs
        if i != len(filenames):
            df.loc['normalized'] = df['normalized'].apply(lambda x: x-i*1/len(filenames))
        else: 
            df.loc['normalized'] = df['normalized'].apply(lambda x: x-1)
            
        ax.plot(df.loc[df['cycle'] == cycle, 'temperature (C)'][:-1],
                 df.loc[df['cycle'] == cycle, 'normalized'][:-1],
                 label=str(name.stem).split('_')[-1].upper(),
                 linewidth=1.25)

        plt.savefig(Path(cwd)/f'{title}.png', dpi=300)
        

def normalize(df):
    df = df.loc[df['time (min)'] > 80.3]
    #TODO: change this from set value to first cycle duration.
    #Unecessary for first implementation, since all cycle lengths identical.
    max_mW = df['heat flow (mW)'].max()
    min_mW = df['heat flow (mW)'].min()
    df.loc['normalized'] = df.loc[:, 'heat flow (mW)'].apply(lambda x: 
        (x-max_mW) / (max_mW - min_mW))
    return df


def cycle_reproducibility(path, odd_heat_cycles=False):
    """Tests to see if the DSC curves look similar between cycles."""
    os.chdir(path)
    filenames = [file for file in glob.glob("*.txt")]
    for polymer in filenames:
        title = polymer.split('_')[-1][:-4].upper()
        plt.title(title)
        df = csv_extraction(polymer)
        heating = df.loc[(df['cycle'] % 2 == 0+odd_heat_cycles) &
                         (df['cycle'] != 0+odd_heat_cycles) &
                         (df['cycle'] != 12-odd_heat_cycles) &
                         (df['time (min)'] > 0)]
        print(heating['cycle'].unique())
        #Following loop finds best way to split up plots
        for coord in range(1, 4, -1):
            if len(filenames) % coord == 0:
                fig, axes = plt.subplots(len(filenames)/coord, coord)
                
        for cycle, ax in zip(heating['cycle'].unique(), axes.flatten()):
            heating.loc[df['cycle'] == cycle].plot(x='temperature (C)', 
                                                   y='heat flow (mW)', ax=ax)
        
        plt.savefig(os.path.join(path, f'{title}.png'))
