from skimage import data, io, filters
from skimage.feature import blob_doh, blob_dog, peak_local_max, canny
from skimage.morphology import watershed
from skimage.restoration import denoise_bilateral
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import label
from scipy import ndimage as ndi
import click
from pathlib import Path
from tqdm import tqdm
import seaborn as sb
import csv
from ncempy.io import dm


def threshold(img):
    """Uses Otsu thresholding to reduce background noise.
    Returns binarized image"""
    thresh = filters.threshold_otsu(img)
    return img > thresh


def rolling_ball(img):
    pass


def watershed_segmentation(img):
    distance = ndi.distance_transform_edt(img)
    local_max = peak_local_max(distance, indices=False)
    plt.plot(local_max)
    plt.show()
    markers = ndi.label(local_max)[0]
    return watershed(-distance, markers, compactness=0.01)


def denoising(img):
    return denoise_bilateral(img, multichannel=False)


def edge_detection(img):
    edges = filters.sobel(img)
    return edges

def get_pixel_ratio(img, img_path):
    try:
        try:
            metadata = dm.dmReader(f'{str(img_path)[:-4]}.dm4')
        except FileNotFoundError:
            metadata = dm.dmReader(f'{str(img_path)[:-4]}.dm3')
        ratio = metadata['pixelSize'][0]
    except FileNotFoundError:
        io.imshow(img)
        plt.show()
        ratio = click.prompt(
            f'dm4 not found. Enter the nm/pixel ratio in {img_path.stem}:',
            type=float, default=0.204)
        plt.close()

    return ratio


def blob_detection(img):
    """Finds maximas in the determinant of the Hessian of the image,
    which corresponds to particles"""
    return blob_doh(img, min_sigma=26, max_sigma=120, num_sigma=25)


def plot_blobs(img, blobs, outpath):
    """Saves masking of blob boundaries on top of original image
     in results subdirectory"""
    fig, ax = plt.subplots()
    ax.set_axis_off()
    plt.tight_layout()
    ax.imshow(img)
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x,y), r, color='r', linewidth=2, fill=False)
        ax.add_patch(c)
    plt.savefig(f'{outpath}_blobs')


def particle_diameters(blobs, ratio):
    diameters = []
    for blob in blobs:
        diameters.append(blob[-1] * 2 * ratio)
    return diameters


def _flatten(nested):
    flat = []
    for lst in nested:
        for item in lst:
            flat.append(item)
    return flat


def plot_kde(result):
    """Plots histogram of particles sizes,
    along with kernel density estimate of distribution"""
    data = np.loadtxt(result)
    plot = sb.distplot(data, axlabel='Diameter (nm)', hist=False)
    plot.figure.savefig(Path(result).with_suffix('.png'), dpi=1200)


def summary_stats(result):
    #TODO: add test to see if analysis passes ISO 13322-1
    print(f'''Average: {sum(result)/len(result)} \nMinimum: {min(result)} 
        \nMaximum: {max(result)} ''')


@click.command()
@click.argument('dir', type=click.Path(exists=True))
def main(dir):
    io.use_plugin('matplotlib')
    output = Path(f'{dir}/Results')
    output.mkdir(parents=True, exist_ok=True)

    print("Processing folder...")
    result_name = click.prompt('Enter result filename', type=str,
                               default=output.parents[0].name)
    csv_name = Path(output / result_name).with_suffix('.csv')

    for idx, img_path in enumerate(Path(dir).glob('**/*.tif')):
        img = io.imread(img_path, as_gray=True)
        ratio = get_pixel_ratio(img, img_path)
        #crop out scale bar
        print('Processing...')
        img = img[:2230, :]
        cleaned = denoising(img)
        blobs = blob_detection(cleaned)

        outpath = Path(dir) / 'Results' / str(idx + 1)
        plot_blobs(img, blobs, outpath)
        plt.show()
        if click.confirm('Is this an acceptable result?'):
            plt.close()
            with open(csv_name, 'a') as f:
                np.savetxt(f, particle_diameters(blobs, ratio))

        else:
            pass

    plot_kde(csv_name)
    print('Finished!')


if __name__ == '__main__':
    main()
