from skimage import data, io, filters
from skimage.feature import blob_doh, peak_local_max
from skimage.morphology import watershed
import numpy as np
import matplotlib.pyplot as plt
# Label image regions.
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import label
from scipy import ndimage as ndi
import click
from pathlib import Path
from tqdm import tqdm


def threshold(img_path):
    """Uses Otsu thresholding to reduce background noise. Returns binarized image"""
    img = io.imread(img_path, as_gray=True, plugin='tifffile')
    print(img.shape)
    thresh = filters.threshold_otsu(img)
    return img > thresh


def rolling_ball(img):
    pass


def watershed_segmentation(img):
    distance = ndi.distance_transform_edt(img)
    print(f'distance: {distance.shape}')
    local_max = peak_local_max(distance, indices=False)
    print(f'Local maxima: {local_max.shape}')
    markers = n di.label(local_max)
    print(f'markers: {markers.shape}')
    return watershed(-distance, markers=markers)

def edge_detection(img):
    edges = filters.sobel(img)
    io.imshow(edges)
    return edges


def blob_detection(img):
    """Finds maximas in the determinant of the Hessian of the image, which should correspond to particles"""
    print('Performing blob detection...')
    return blob_doh(img, max_sigma=250, threshold=0.018)


def blob_overlay(img, blobs, outpath):
    """Saves masking of blob boundaries on top of original image in results subdirectory"""
    fig, ax = plt.subplots()
    ax.imshow(img)
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x,y), r, color='r', linewidth=2, fill=False)
        ax.add_patch(c)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(outpath)


def scale_bar(img):
    pass


def particle_diameters(blobs):
    pass

def pdi_histogram(combined_diameters):
    pass


@click.command()
@click.argument('dir', type=click.Path(exists=True))
def main(dir):
    Path(f'{dir}/Results').mkdir(parents=True, exist_ok=True)
    print("Processing folder...")
    for idx, img_path in enumerate(Path(dir).glob('*.tif')):
        img = io.imread(img_path, as_gray=True)
        #crop out scale bar
        img = img[:2230, :]
        segmented = watershed_segmentation(img)
        blobs = blob_detection(segmented)
        outpath = Path(dir) / 'Results' / str(idx+1)
        print(str(outpath), type(outpath))
        overlay(img, blobs, outpath)


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
