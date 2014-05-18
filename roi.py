from box import Box
import sys
from math import sqrt
import cv2 as cv
import numpy as np

def findRoi(filename):

	image = cv.imread(filename)
	image = cv.resize(image, (0, 0), fx = 0.2, fy = 0.2) # TODO: Just set a general bound on image size

	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

	LOWAREA_THRESH = 10 
	UPAREA_THRESH = 3000
	contours, heirachy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

	contours = [con for con in contours if LOWAREA_THRESH < cv.contourArea(con) < UPAREA_THRESH]
	contours = [cv.approxPolyDP(con, 10, True) for con in contours]
	contours = [cv.convexHull(con) for con in contours]
	contours = [con for con in contours if len(con) != 1]

	# After initialization, follow this algorithm:
	# 1. Consider a box B in the set.
	# 2. For every other box C in the set
	# 3. If dist(B, C) < THRESHOLD, meld B's set with C's set
	# 4. Repeat for each box C
	# 5. For each disjoint set, meld each box in the set together. These are your clusters.

	objects = []
	for i, con in enumerate(contours):
		x, y, w, h = cv.boundingRect(con)
		box = Box(x, y, w, h)
		objects.append({"box": box, "set": set([i]), "id": i})

	THRESH = 12 
	AREA_THRESH = 200
	SMALL_DIST_THRESH = 15 
	for obj1 in objects:
		for obj2 in objects:

			# If the box is not in box 1's cluster yet
			if obj2["id"] not in obj1["set"]:
				area1 = obj1["box"].area()
				area2 = obj2["box"].area()
				if obj1["box"].dist(obj2["box"]) < THRESH:

				# TODO: Need to fix these bugs
				#	if obj1["box"].dist(obj2["box"]) != obj2["box"].dist(obj1["box"]):
				#		print "WARNING: Antisymmetric distance for {0} and {1}".format(obj1["id"], obj2["id"])
				#		print "Distances are: {0} and {1}".format(obj1["box"].dist(obj2["box"]), obj2["box"].dist(obj1["box"]))
				#		print "{0}, {1}".format(obj1["box"], obj2["box"])
					
					obj1["set"] = obj1["set"].union(obj2["set"])
					for id in obj1["set"]:
						objects[id]["set"] = obj1["set"] # Shallow copy; all point to obj1's set
	

	# Groups the members of the clusters together
	clusters = set([tuple(obj["set"]) for obj in objects])
	outputBoxes = []
	for tup in clusters:
		boxes = [objects[i]["box"] for i in tup]
		outputBoxes.append(Box.meld(*boxes))
	outputBoxes = [box.getContourRep() for box in outputBoxes]

	PADDING = 5
	return [image[box[2][0][1]-PADDING:box[0][0][1]+PADDING, box[1][0][0]-PADDING:box[0][0][0]+PADDING] for box in outputBoxes]

