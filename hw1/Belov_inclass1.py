import os

from skimage import io
from skimage.morphology import dilation, disk
from skimage.feature import canny, match_template
from skimage.transform import rescale, resize, ProjectiveTransform, warp, hough_line, hough_line_peaks

import numpy as np
import cv2


SUDOKU_SHAPE = 500
ITEM_REDUCE_COEFF = 0.88

PATH_TO_TEMPLATES = 'templates'
IMG_FORMATS = ['jpg', 'jpeg', 'png']


def get_tform_points(current_points):
    """Return desired points for ProjectiveTransform."""
    
    #Firstly we should sort the corner's point
    current_points[:2] = np.array(sorted(current_points[:2], key=lambda x: x[1]))
    current_points[2:] = np.array(sorted(current_points[2:], key=lambda x: x[1]))

    a = current_points[:2][:, 0].mean()
    c = current_points[2:][:, 0].mean()
    b = current_points[::2][:, 1].mean()
    d = current_points[1::2][:, 1].mean()

    desired_points = [[a, b], [a, d], [c, b], [c, d]]
    desired_points = np.array(desired_points, dtype=np.int32)

    return desired_points


def find_corners(image):
    edges = canny(image)
    selem = disk(1)
    edges = dilation(edges, selem)
    
    edges = (edges).astype(np.uint8)
    ext_contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour = max(ext_contours, key=cv2.contourArea)
    contour = contour.squeeze()

    epsilon = 0.05 * cv2.arcLength(contour, True)
    corners = cv2.approxPolyDP(contour, epsilon, True).squeeze()

    return corners


def transform_image(image, corners):
    corners = sorted(corners, key=lambda x: x[0])
    corners = np.array(corners)

    desired_corners = get_tform_points(corners)

    tform = ProjectiveTransform()
    tform.estimate(desired_corners, corners)
    image_warped = warp(image, tform)

    return image_warped, desired_corners


def crop_image(image, corners):
    left, bot = corners.min(axis=0)
    right, top = corners.max(axis=0)

    image_cropped = image[bot: top, left:right]
    side = max(image_cropped.shape)

    image_cropped = resize(image_cropped, (side, side),
                           anti_aliasing=True)
    image_cropped = rescale(image_cropped, SUDOKU_SHAPE/side)

    return image_cropped


def normalize_image(image):
    corners = find_corners(image)
    image_warped, desired_corners = transform_image(image, corners)
    image_cropped = crop_image(image_warped, desired_corners)
    
    return image_cropped


def get_sudoku_items(image):
    size_d = round(SUDOKU_SHAPE/9)
    size_dig = round(size_d*ITEM_REDUCE_COEFF)
    shift = (size_d - size_dig) // 2
    sudoku = np.zeros((9, 9, size_dig, size_dig))

    for i in range(9):
        for j in range(9):
            digit_img = image[i*size_d:(i+1)*size_d, j*size_d:(j+1)*size_d].copy()
            digit_img = digit_img[shift: shift+size_dig, shift: shift+size_dig]

            threshold = np.median(digit_img)*0.9
            digit_img[digit_img>threshold] = 1
            sudoku[i, j] = digit_img

    return sudoku


def get_image_paths(path):
    is_img = lambda x: any(x.endswith(format) for format in IMG_FORMATS)

    files = os.listdir(path)
    files = map(str.lower, files)
    files = filter(is_img, files)
    image_paths = [os.path.join(path, s) for s in files]

    return image_paths


def load_templates():
    templates_paths = get_image_paths(PATH_TO_TEMPLATES)
    templates_paths.sort()

    templates = {i: [] for i in range(1, 10)}

    for i, t in enumerate(templates_paths):
        template = io.imread(t, as_gray=True)
        template = rescale(template, 0.95)
        templates[i//2+1].append(template)
    
    return templates


def find_max_digits_corr(digit, templates):
    max_digits_corr = np.zeros(9)
    for d, templs in templates.items():
        max_corr = 0
        for t in templs:
            res = match_template(digit, t)
            max_corr += res.max()
        max_digits_corr[d-1] = max_corr
        
    return max_digits_corr


def recognize_digits(image, threshold=1.2):
    sudoku = get_sudoku_items(image)
    templates = load_templates()

    digits = np.zeros((9, 9), dtype=np.uint8)

    for i in range(9):
        for j in range(9):
            max_digits_corr = find_max_digits_corr(sudoku[i, j], templates)
            digits[i, j] = np.argmax(max_digits_corr) + 1 if max_digits_corr.max() > threshold else 0
    
    return digits
