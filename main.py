#!/usr/bin/python
import cv2 as cv
import numpy as np
import sys
import glob
import multiprocessing
import roi

#TODO: Integrate with Henry's Code
#Get score
#Work on getting scale down
MIN_MATCH_COUNT = 4
DATAPATH = "./data/standard/*"
FILE = "./data/demo-images/scattered4.jpg"


def findInlier(img):
	# Initiate SIFT detector

	img1 = img[0]		# Image in question
	img2 = img[1][0] 	# Gold standard image
	sift = cv.SIFT()

	kp1, des1 = sift.detectAndCompute(img1, None)
	kp2, des2 = sift.detectAndCompute(img2, None)

	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
	search_params = dict(checks=50)

	flann = cv.FlannBasedMatcher(index_params, search_params)

	matches = flann.knnMatch(des1, des2, k=2)

	# Store all good matches as per Lowe's ratio test.
	good = [m for m, n in matches if m.distance < 0.7*n.distance]

	if len(good) > MIN_MATCH_COUNT:
		src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
		dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

		M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
		matchesMask = mask.ravel().tolist()

	else:
		#print "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
		matchesMask = []

	# Print Inliers
	return (len(matchesMask), img[1][1])


#Gets the nearest neighbor for each tile in
#a list of ROI tiles to the testData
def NN(tiles, testData):
	"""param tiles: The regions of interest, in the form of images.
	param testData: Array of 30 or forty images.
	"""
	#store the max inliers for each tile
	maxInliers = []
	for tile in tiles:

		pairs = [(tile.copy(), img2) for img2 in testData]
		if False:
			p = multiprocessing.Pool(processes = 4)
			inliers = p.map(findInlier, pairs)
		else:
			inliers = [findInlier(pair) for pair in pairs]

		theMax = max(inliers)
		guess = cv.imread(theMax[1])
		maxInliers.append(theMax)


#Converts a list of image names into a list of
#tuple's where the first value of the tuple is 
#the OpenCV image and the second value of the 
#tuple is the file name
def getImage(files):
	return [(cv.resize(cv.imread(f),(0,0), fx = 0.2, fy = 0.2), f) for f in files]

def main():
	#Get images

	#get list of images in golden data set
	# Obtains the array of images to the golden standards
	testData = glob.glob(DATAPATH)
	images = getImage(testData)
	
	#REMOVE ONCE HENRY'S DONE
	# tiles contains an array of images
	tiles = roi.findRoi(FILE)
	inliers = NN(tiles, images)

if __name__ == "__main__":
	main()
