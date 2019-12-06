import numpy as np


def rigid_transform_3d(xs, ys):
    """
    expects 2 arrays of shape (3, N)

    rigid transform algorithm from
    http://nghiaho.com/?page_id=671
    """
    assert xs.shape == ys.shape
    assert xs.shape[0] == 3, 'The points must be of dimmensionality 3'

    # find centroids and H
    x_centroid = xs.mean(axis=1)[:, np.newaxis]
    y_centroid = ys.mean(axis=1)[:, np.newaxis]
    H = (xs - x_centroid) @ (ys - y_centroid).T

    # find rotation
    U, S, Vt = np.linalg.svd(H)
    rotation = Vt.T @ U.T

    # handling reflection
    if np.linalg.det(rotation) < 0:
        Vt[2, :] *= -1
        rotation = np.dot(Vt.T, U.T)

    # find translation
    translation = y_centroid - rotation @ x_centroid

    return translation, rotation


# custom model class for skimage's ransac
class Translation:
    def __init__(self):
        self.R = np.eye(3)
        self.t = np.zeros(3)

    def estimate(self, src, dst):
        self.t, self.R = rigid_transform_3d(src.T, dst.T)

    def residuals(self, src, dst):

        assert len(src) == len(dst)
        residuals = np.zeros(len(src))

        for i, (p1, p2) in enumerate(zip(src, dst)):
            diff = np.dot(self.R, p1) + self.t - p2
            residuals[i] = np.linalg.norm(diff)

        return residuals
