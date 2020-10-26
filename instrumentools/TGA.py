# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 16:39:19 2016

@author: dendrondal
"""

import glob
import os
import re
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
from cycler import cycler
from matplotlib import ticker


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
        df = pd.read_excel(f"{cwd}/{name}", skiprows=20)
        TG_ = [100]
        # converts raw mass measurements into % decomposition
        for j in range(1, len(df["ug"])):
            TG_.append((df["ug"][j] / df["ug"][0]) * 100)
        df["TG(Percent)"] = TG_
        # list of decomposition temps is made to use in plot labels or output.
        decomposition.append(
            df.loc[df["TG(Percent)"].apply(lambda x: int(x)) == 95, "Cel"].mean()
        )

        # Previously used plotting parameters are greyed out. May still be wanted.
        # plt.title(title, family='arial', weight='bold')
        plt.xlabel("Temperature", family="arial", weight="bold", size=10)
        # plt.xticks(np.arange(df['Cel'].min(), df['Cel'].max(),10),
        #           labels=None)
        plt.ylabel("%TG", family="arial", weight="bold", size=10)
        # plt.yticks(np.arange(df['TG(Percent)'].min(), df['TG(Percent)'].max(),1),
        #           labels=None)
        # fig.patch.set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        # ax.axis('off')
        plt.plot(df["Cel"], TG_, label=f"{name[:-4].upper()}", linewidth=2)
        plt.tight_layout()
        plt.legend()
        plt.savefig(os.path.join(cwd, f"{title}.png"), dpi=1440)

    return decomposition


@click.command()
@click.option(
    "--path",
    prompt="Folder containing TGA data",
    type=click.Path(exists=True),
    default=os.getcwd(),
)
@click.option("--title", prompt="Plot title")
def main(path, title):
    return tga_plot(path, title)


if __name__ == '__main__':
    main()
