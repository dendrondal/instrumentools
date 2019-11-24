from .TEM import get_pixel_ratio, threshold, blob_detection, plot_blobs
from skimage.io import imread
from skimage.util import crop


def img_subsampling(test_img_path):
    full_img = imread(test_img_path)
    q1 = crop(full_img, [(0, 300), (0, 300)])
    q2 = crop(full_img, [(600, 900), (600, 900)])
    q3 = crop(full_img, [(1200, 1500), (1200, 1500)])
    return [q1, q2, q3]


def fitness_function(diameters, size_estimate):
    mse = 1/len(diameters)*sum([(size_estimate - y)**2 for y in diameters])
    fitness = len(diameters) / mse
    return fitness
