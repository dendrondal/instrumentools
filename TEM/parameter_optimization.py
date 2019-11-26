from TEM import get_pixel_ratio, denoising, particle_diameters
from skimage.io import imread
from collections import namedtuple
from skimage.feature import blob_doh
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
from pathlib import Path


def img_subsampling(test_img_path):
    full_img = imread(test_img_path, as_gray=True)
    q1 = full_img[0:1000, 0:1000]
    q2 = full_img[1000:2000, 1000:2000]
    q3 = full_img[2000:3000, 2000:3000]
    return [q1, q2, q3]


def fitness_function(diameters, size_estimate):

    mse = 1/len(diameters)*sum([(size_estimate - y)**2 for y in diameters])
    fitness = len(diameters) / mse
    return 1/fitness


def optimization(epochs=25):
    path = Path('/home/dal/Pictures/190612_tem/pbzma/Dal1_UrF_6000X_0110.tif')
    result = dict()
    ratio = get_pixel_ratio(imread(path, as_gray=True), path)
    for _ in tqdm(range(epochs)):
        min_sigma = random.choice(range(1, 35))
        max_sigma = random.choice(range(40, 140))
        sample = img_subsampling(path)[1]
        blobs = blob_doh(sample,
                         min_sigma=min_sigma,
                         max_sigma=max_sigma,
                         num_sigma=42)
        diameters = particle_diameters(blobs, ratio)
        fitness = fitness_function(diameters, 100)
        result[f'min={min_sigma}_max={max_sigma}'] = fitness
    return result




