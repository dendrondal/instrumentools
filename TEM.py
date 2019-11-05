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
    """Uses Otsu t0hresholding to reduce background noise. Returns binarized image"""
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


def blob_detection(img):
    """Finds maximas in the determinant of the Hessian of the image, which should correspond to particles"""
    return blob_doh(img, threshold=0.016, max_sigma=133)


class Overlay:
    def __init__(self, img, outpath):
        self.img = img
        self.outpath = outpath
        self.fig, self.ax = plt.subplots()
        self.ax.set_axis_off()
        plt.tight_layout()

    def blob(self, blobs):
        """Saves masking of blob boundaries on top of original image in results subdirectory"""
        self.ax.imshow(self.img)
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x,y), r, color='r', linewidth=2, fill=False)
            self.ax.add_patch(c)
        plt.savefig(f'{self.outpath}_blobs')

    def sobel_edge(self, edgemap):
        self.ax.imshow(edgemap)
        plt.savefig(f'{self.outpath}_edges')


def scale_bar(img):
    pass


def particle_diameters(blobs, ratio):
    diameters = []
    for blob in blobs:
        diameters.append(blob[-1] * 2 * ratio)
    return diameters


def population_sample():
    pass


def fitness_function(diameters, size_estimate):
    mse = 1/len(diameters)*sum([(size_estimate - y)**2 for y in diameters])
    fitness = len(diameters) / mse
    return fitness


def _flatten(nested):
    flat = []
    for lst in nested:
        for item in lst:
            flat.append(item)
    return flat


def plot_kde(result):
    data = np.loadtxt(result)
    plot = sb.distplot(data, axlabel='Diameter (nm)', hist=False)
    plot.figure.savefig(Path(result).with_suffix('.png'), dpi=1200)


def summary_stats(result):
    print(f'''Average: {sum(result)/len(result)} \nMinimum: {min(result)} 
        \nMaximum: {max(result)} ''')



@click.command()
@click.argument('dir', type=click.Path(exists=True))
def main(dir):

    output = Path(f'{dir}/Results')
    output.mkdir(parents=True, exist_ok=True)

    print("Processing folder...")
    result_name = click.prompt('Enter result filename', type=str,
                               default=output.parents[0].name)
    csv_name = Path(output / result_name).with_suffix('.csv')

    imgs = [i for i in Path(dir).glob('**/*.tif')]
    for idx, img_path in tqdm(enumerate(imgs), total=len(imgs)):
        img = io.imread(img_path, as_gray=True)

        try:
            metadata = dm.dmReader(f'{str(img_path)[:-4]}.dm4')
            ratio = metadata['pixelSize'][0]
        except FileNotFoundError:
            ratio = click.prompt(
                f'dm4 not found. Enter the nm/pixel ratio in {img_path.stem}:',
                type=float, default=0.204)

        #crop out scale bar
        img = img[:2230, :]
        cleaned = denoising(img)
        blobs = blob_detection(cleaned)

        with open(csv_name, 'a') as f:
            np.savetxt(f, particle_diameters(blobs, ratio))

        outpath = Path(dir) / 'Results' / str(idx+1)
        Overlay(img, outpath).blob(blobs)

    plot_kde(csv_name)
    print('Finished!')


if __name__ == '__main__':
    main()



# imgPath = 'C:/Users/Amirber/Documents/pm25/farc_snd6_(c6).jpg'
# # Insert a um to pixel conversion ratio
# um2pxratio = 1
# image = imread(imgPath, 0)  # data.coins()  # or any NumPy array!
# # remove the 2 um scake
# image = image[:800, :]
# # Whole image
# io.imshow(image)
#
# # Show histogram
# values, bins = np.histogram(image,
#                             bins=np.arange(256))
# plt.figure()
# plt.plot(bins[:-1], values)
# plt.title("Image Histogram")
# plt.show()
#
# # Calculate Soble edges
# edges_sob = filters.sobel(image)
# io.imshow(edges_sob)
#
# # Show histogram of non-sero Sobel edges
# values, bins = np.histogram(np.nonzero(edges_sob),
#                             bins=np.arange(1000))
# plt.figure()
# plt.plot(bins[:-1], values)
# plt.title("Use Histogram to select thresholding value")
#
# # Using a threshold to binarize the images, consider replacing with an adaptive
# # criteria. raising the TH to 0.03 will remove the two touching particles but will
# # cause larger particles to split.
# edges_sob_filtered = np.where(edges_sob > 0.01, 255, 0)
# io.imshow(edges_sob_filtered)
#
# # Use label on binary Sobel edges to find shapes
# label_image = label(edges_sob_filtered)
# fig, ax = plt.subplots(1, figsize=(20, 10))
# ax.imshow(image, cmap=plt.cm.gray)
# ax.set_title('Labeled items', fontsize=24)
# ax.axis('off')
#
# # Do not plot regions smaller thn 5 pixels on each axis
# sizeTh = 4
#
# for region in regionprops(label_image):
#     # Draw rectangle around segmented coins.
#     minr, minc, maxr, maxc = region.bbox
#     rect = mpatches.Rectangle((minc, minr),
#                               maxc - minc,
#                               maxr - minr,
#                               fill=False,
#                               edgecolor='red',
#                               linewidth=2)
#     ax.add_patch(rect)
#
# # Sort all found shapes by region size
# sortRegions = [[(region.bbox[2] - region.bbox[0]) * (region.bbox[3] - region.bbox[1]), region.bbox]
#                for region in regionprops(label_image) if
#                ((region.bbox[2] - region.bbox[0]) > sizeTh and (region.bbox[3] - region.bbox[1]) > sizeTh)]
# sortRegions = sorted(sortRegions, reverse=True)
#
# # Check particle sizes distribution
# particleSize = [size[0] for size in sortRegions]
#
# # Show histogram of non-sero Sobel edges
# plt.figure()
# plt.plot(np.multiply(np.power(um2pxratio, 2), particleSize), linewidth=2)
# plt.xlabel('Particle count', fontsize=14)
# plt.ylabel('Particle area', fontsize=14)
# plt.title("Particle area distribution", fontsize=16)
# # Show 5 largest regions location, image and edge
# for region in sortRegions[:5]:
#     # Draw rectangle around segmented coins.
#     minr, minc, maxr, maxc = region[1]
#     fig, ax = plt.subplots(1, 3, figsize=(15, 6))
#     ax[0].imshow(image, cmap=plt.cm.gray)
#     ax[0].set_title('full frame', fontsize=16)
#     ax[0].axis('off')
#     rect = mpatches.Rectangle((minc, minr),
#                               maxc - minc,
#                               maxr - minr,
#                               fill=False,
#                               edgecolor='red',
#                               linewidth=2)
#     ax[0].add_patch(rect)
#
#     ax[1].imshow(image[minr:maxr, minc:maxc], cmap='gray')
#     ax[1].set_title('Zoom view', fontsize=16)
#     ax[1].axis("off")
#     ax[1].plot([0.1 * (maxc - minc), 0.3 * (maxc - minc)],
#                [0.9 * (maxr - minr), 0.9 * (maxr - minr)], 'r')
#     ax[1].text(0.15 * (maxc - minc), 0.87 * (maxr - minr),
#                str(round(0.2 * (maxc - minc) * um2pxratio, 1)) + 'um',
#                color='red', fontsize=12, horizontalalignment='center')
#
#     ax[2].imshow(edges_sob_filtered[minr:maxr, minc:maxc], cmap='gray')
#     ax[2].set_title('Edge view', fontsize=16)
#     ax[2].axis("off")
#     plt.show()
#
# # Show 5 smallest regions location, image and edge
# for region in sortRegions[-5:]:
#     # Draw rectangle around segmented coins.
#     minr, minc, maxr, maxc = region[1]
#     fig, ax = plt.subplots(1, 3, figsize=(15, 6))
#     ax[0].imshow(image, cmap=plt.cm.gray)
#     ax[0].set_title('full frame', fontsize=16)
#     ax[0].axis('off')
#     rect = mpatches.Rectangle((minc, minr),
#                               maxc - minc,
#                               maxr - minr,
#                               fill=False,
#                               edgecolor='red',
#                               linewidth=2)
#     ax[0].add_patch(rect)
#
#     ax[1].imshow(image[minr:maxr, minc:maxc], cmap='gray')
#     ax[1].set_title('Zoom view', fontsize=16)
#     ax[1].axis("off")
#     ax[1].plot([0.1 * (maxc - minc), 0.3 * (maxc - minc)],
#                [0.9 * (maxr - minr), 0.9 * (maxr - minr)], 'r')
#     ax[1].text(0.15 * (maxc - minc), 0.87 * (maxr - minr),
#                str(round(0.2 * (maxc - minc) * um2pxratio, 1)) + 'um',
#                color='red', fontsize=12, horizontalalignment='center')
#
#     ax[2].imshow(edges_sob_filtered[minr:maxr, minc:maxc], cmap='gray')
#     ax[2].set_title('Edge view', fontsize=16)
#     ax[2].axis("off")
#     plt.show()
