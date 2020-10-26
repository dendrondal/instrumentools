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


def csv_extraction(path, save=False):
    """Takes in .txt file output by TA software and parses into individual
    cyles. If save boolean is true, saves .csv version of file
    with same name as TA .txt output."""
    with open(path, encoding="utf-16") as f:
        for i, line in enumerate(f):
            if "OrgFile" in line:
                # Some files are output with different starting lines.
                start = i + 1
                break
            else:
                start = 68
                # default starting line for output data
        df = pd.read_csv(
            path, delim_whitespace=True, skiprows=start, header=None, encoding="utf-16"
        )

    df.columns = [
        "time (min)",
        "temperature (C)",
        "heat flow (mW)",
        "heat capacity (mJ/C)",
        "N2 flow",
    ]

    num = 0

    def cycle(x):
        nonlocal num
        if x["time (min)"] == -2:
            # for some reason, this denotes a switch between heating/cooling
            num = x["temperature (C)"]
        return num

    df["cycle"] = df.apply(cycle, axis=1)
    if save:
        df.to_csv(path.with_suffix(".csv"))

    return df


def save_multiple_csvs(cwd):
    os.chdir(cwd)
    for file in glob.glob("*.txt"):
        csv_extraction(file, save=True)


def _dsc_plot_setup(legend):
    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    ax.set_prop_cycle(cycler("color", ["y", "g", "b", "r"]))
    # Plot formatting goes here
    plt.xlabel("Temperature ($^o$C)", family="arial", weight="bold", size=8)
    plt.ylabel("Heat Flow (mW)", family="arial", weight="bold", size=8)
    minor_locator = ticker.AutoMinorLocator()
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(4))
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.tick_params(axis="both", which="major", labelsize=6)
    # custom y-axis, if needed:
    # ax.set_ylim([-1, -0.6])
    plt.tight_layout()

    return fig, ax


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
    cycle = float(cycle)
    fig, ax = _dsc_plot_setup(legend)

    if filenames is None:
        filenames = [file for file in Path(cwd).glob("*.txt")]
    elif type(filenames) is str:
        filenames = list(filenames)
    else:
        raise TypeError("filenames must be list of strings or None.")

    for i, name in enumerate(filenames):
        print(f"Processing {name.stem}...")
        df = csv_extraction(name)
        df = normalize(df, cycle)
        # This operation introduces offset between the graphs
        df["normalized"] = df["normalized"].apply(lambda x: x - i * 1 / len(filenames))
        if len(df.loc[df["cycle"] == cycle, "temperature (C)"][:-1]) == 0:
            raise Exception(
                "Invalid cycle specified. Please use enter a cycle between {} and {}".format(
                    df["cycle"].min(), df["cycle"].max()
                )
            )
        label = str(name.stem).split("_")[1]
        ax.plot(
            df.loc[df["cycle"] == cycle, "temperature (C)"][:-1][1:],
            df.loc[df["cycle"] == cycle, "normalized"][:-1][1:],
            label=label,
            linewidth=1.25,
        )
    if legend:
        ax.legend(prop={"size": 6}, frameon=False)

    plt.savefig(Path(cwd) / f"{title}.png", dpi=300)


def normalize(df, cycle):
    min_mW = df.groupby([df["cycle"] == cycle]).min()["heat flow (mW)"][1]
    max_mW = df.groupby([df["cycle"] == cycle]).max()["heat flow (mW)"][1]
    if min_mW == max_mW:
        cycle += 1
        print(f"Dummy cycle specified. Trying cycle {cycle} instead")
    # Getting rid of settingwithcopy warning, since it doesn't matter here
    pd.options.mode.chained_assignment = None
    df["normalized"] = df.loc[:, "heat flow (mW)"].apply(
        lambda x: (x - max_mW) / (max_mW - min_mW)
    )
    return df


def cycle_reproducibility(path, odd_heat_cycles=False):
    """Tests to see if the DSC curves look similar between cycles."""
    os.chdir(path)
    filenames = [file for file in glob.glob("*.txt")]
    for polymer in filenames:
        title = polymer.split("_")[-1][:-4].upper()
        plt.title(title)
        df = csv_extraction(polymer)
        heating = df.loc[
            (df["cycle"] % 2 == 0 + odd_heat_cycles)
            & (df["cycle"] != 0 + odd_heat_cycles)
            & (df["cycle"] != 12 - odd_heat_cycles)
            & (df["time (min)"] > 0)
        ]
        # Following loop finds best way to split up plots
        for coord in range(1, 4, -1):
            if len(filenames) % coord == 0:
                fig, axes = plt.subplots(len(filenames) / coord, coord)

        for cycle, ax in zip(heating["cycle"].unique(), axes.flatten()):
            heating.loc[df["cycle"] == cycle].plot(
                x="temperature (C)", y="heat flow (mW)", ax=ax
            )

        plt.savefig(os.path.join(path, f"{title}.png"))


@click.command()
@click.option(
    "--path",
    prompt="Folder containing DSC data",
    help="Folder containing DSC data",
    type=click.Path(exists=True),
    default="/home/dal/Documents/jsdw_191217_pisa-dsc",
)
@click.option("--title", prompt="Plot title")
@click.option("--cycle", prompt="Cycle number to plot")
def main(path, title, cycle):
    leg = click.confirm("Include legend?")
    return dsc_plotting(path, title, cycle, legend=leg)


if __name__ == "__main__":
    main()
