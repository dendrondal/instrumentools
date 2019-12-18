from thermal_analysis import dsc_plotting, tga_plot
import click
import os


@click.command()
@click.option('--path', prompt='Folder containing TGA data',
            type=click.Path(exists=True), default=os.getcwd())
@click.option('--title', prompt='Plot title')
def tga_cli(path, title):
    return tga_plot(path, title)


@click.command()
@click.option('--path', prompt='Folder containing DSC data',
            type=click.Path(exists=True), default=os.getcwd())
@click.option('--title', prompt='Plot title')
@click.option('--cycle', prompt='Cycle number to plot')
def dsc_cli(path, title, cycle):
    leg = click.confirm('Include legend?')
    return dsc_plotting(path, title, cycle, legend=leg)


@click.command()
@click.option('--plot_type', prompt='What type of thermal data are you analyzing?')
def main(plot_type):
    features = {'TGA': tga_cli, 'DSC': dsc_cli}
    try:
            features[plot_type.upper()].__call__
    except KeyError as e:
        raise Exception(f'Data type not yet supported.\
             Valid data types are {[key for key in features.keys()]}')


if __name__ == '__main__':
    main()