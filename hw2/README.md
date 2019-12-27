## Task

Given a series of RGBD (D for depth) images, determine the trajectory of the camera in the local coordinates of the first (starting) image. The expected results are 

(1) The recovered 2D camera trajectory (seen from above).

(2) The starting image with an overlaid line, denoting the trajectory.

The dataset can be found [here](https://drive.google.com/file/d/1Dev-uoW2LJCNGB8cOSeL86hqj9HEGVet/view?usp=sharing).

 

## Grading details

1. Find key points on an image (2 points).
2. Choose two consecutive images and match their keypoints (2 points).
3. Transfer detected keypoints coordinates to the real world coordinates (4 points).
4. Determine the translation vector and rotation matrix for the same 2 images using RANSAC. The partial code for this task is here (4 points)
5.  Find translation vectors and rotation matrices for all pairs of consecutive images (2 points)
6. Skip an image if it creates a bad translation vector (2 points)
7. Convert all translations vectors to the coordinate system of the first image (1 point)
8. Draw the camera trajectory with a view from above (1 point)
9. Draw the camera trajectory on the first image (2 points)

 

## Additional notes

1. SIFT is a proprietary algorithm not shipped with the standard `opencv-python` library. In order to use it uninstall `opencv-python` and install `opencv-contrib-python`: `pip install opencv-contrib-python==3.4.0.14`.
2. To translate coordinates between the world coordinate space (x,y,z) and the camera coordinate space (u, v in pixels), you may refer to https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html (Links to an external site.)
3. You will need the matrix of the camera's intrinsic parameters. It's saved in the file camera_matrix.json
4. The depth images are single-channel 16 bit. Every pixel contains the depth in millimeters to the corresponding point. To read it, use OpenCV imread with the flag IMREAD_UNCHANGED.
5. Take a look at several depth images. Sometimes they are noisy since the camera wasn't able to compute depth at certain points. The right way to estimate camera displacement is to ignore these points. 
6. We found the image number 740 to be blurred, and it spoiled our algorithm. We recommend you to ignore this image in your code. Also, you may ignore the first 100 images if you find this useful.
