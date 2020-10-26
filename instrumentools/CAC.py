# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:08:18 2016

@author: dendrondal
"""
import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import style

style.use("bmh")


@click.command()
@click.option(
    "--path",
    prompt="Full path to .csv file",
    help="Full path to .csv file",
    type=click.Path(exists=True),
)
@click.option(
    "--wv_range",
    prompt="Range of wavelengths (i.e. max - min)",
    help="Range of wavelengths (i.e. max - min)",
)
@click.option(
    "--min_conc",
    prompt="Minimum concentration, in mg/mL",
    help="Minimum concentration, in mg/mL",
)
@click.option(
    "--max_conc",
    prompt="Maximum concentration, in mg/mL",
    help="Maximum concentration, in mg/mL",
)
@click.option(
    "--step",
    prompt="Total number of samples in csv",
    help="Total number of samples in csv",
)
@click.option(
    "--vb1",
    prompt="Lambda max/first vibronic band",
    help="Lambda max/first vibronic band",
)
@click.option(
    "--vb3",
    prompt="Third vibronic band",
    required=False,
    help="If you are comparing the first and third vibronic band for\
              a dye, (i.e. pyrene), enter it here. Otherwise, just press enter",
)
def main(path, wv_range, min_conc, max_conc, step, vb1, vb3=None):
    """
    Graphs .csv output from Bruker UV-Vis software. Outputs stacked UV-vis
    spectra and wavelength (or wavelength raio, depending on dye) vs.
    log(concentration) spectra as .png files in the same directory as .csv file.
    """
    # creates and saves overlapping UV-vis spectra for each sample
    df = pd.read_csv(path, header=None, skiprows=2)
    even_cols = [col for col in range(2, len(df.columns)) if col % 2 == 0]
    # removes all even columns past index 0, corresponding to wavelength repeats
    df = df.drop(even_cols, 1)
    df = df[: wv_range + 1]
    df = df.convert_objects(convert_numeric=True)
    conc = np.linspace(min_conc, max_conc, step)
    plt.figure(figsize=(10, 7))
    for i in range(1, len(conc) + 1, 2):
        plt.plot(df[0].values, df[i].values, label=i)
    abs_vb1 = df[df[0] == vb1].values
    plt.savefig(f"{path[:-4]}_stacked_UV-vis.png")
    plt.show()
    # creates CAC graphs with lambda max or 1st and 3rd vibronics
    log_conc = [np.log(value) for value in conc]
    plt.figure(figsize=(10, 7))
    plt.xlabel("ln(Concentration (mg/mL))")
    if not vb3:
        plt.ylabel(f"Absorbance intensity: {vb1} nm")
        plt.plot(log_conc, abs_vb1[0, 1:], marker="*")
    else:
        df["ratio"] = df[df[0] == vb1] / df[df[0] == vb3]
        plt.ylabel(f"I{vb1}/I{vb3}")
        plt.plot(log_conc, df["ratio"].values, marker="*")
    plt.savefig(f"{path[:-4]}_cac.png")
    plt.show()


if __name__ == "__main__":
    main()
