Introduction
======================
This is a project me and my friend Rahul Datta contributed to while taking our graduate level computer vision class. It implements a system that allows one to identify mahjong tiles from a given image.

We built our system over the computer vision API, OpenCV.

Methods
======================
To segement the images, we used a bounding box method. Essentially, two tiles could be segmented if it was possible to draw a bounding box around each one of them.

After segmentation, we found a homography of best fit between an image I and a set of corresponding images for other tiles.

Installation
======================
This is largly untested, but I put all of the dependences into requirements.txt. To install these dependencies, run

`sudo pip install -r requirements.txt`

You might run into other installation errors.
