"""
Defines the contour object. This should theoretically be easier to manipulate
than the contours provided by numpy.
"""
from math import sqrt
from colorama import *
import numpy as np
from cv2 import convexHull
class Box():

	@classmethod
	def create(cls, boxCon):
		"""Creates a box from a contour representation of the box."""
		array = boxCon.tolist()
		startX = min(boxCon, key = lambda vertex : vertex[0][0])[0][0]
		endX = max(boxCon, key = lambda vertex : vertex[0][0])[0][0]
		startY = min(boxCon, key = lambda vertex : vertex[0][1])[0][1]
		endY = max(boxCon, key = lambda vertex : vertex[0][1])[0][1]
		box = cls(startX, startY, endX - startX, endY - startY)
		return box
	
	def __init__(self, x, y, width, height):
		if width < 0 or height < 0:
			print( Fore.RED + "WARNING: Width or height is less than 0." + Fore.RESET )
		elif x < 0 or height < 0:
			print( Fore.RED + "WARNING: x or y is less than 0." + Fore.RESET )

		self.startX = x
		self.startY = y
		self.endX = x + width
		self.endY = y + height


	@classmethod
	def meld(cls, * boxes):
		"""Takes in at least one other Box instance, and puts them together.

		The larger box is defined to have the top, bottom, left, and right most
		extreme points of the other boxes.
		"""
		startX = min(boxes, key = lambda box : box.startX).startX
		endX = max(boxes, key = lambda box : box.endX).endX
		startY= min(boxes, key = lambda box : box.startY).startY
		endY= max(boxes, key = lambda box : box.endY).endY
		return Box(startX, startY, endX - startX, endY - startY)

	def __repr__(self):
		return "[{0}, {1}] x [{2}, {3}]".format(self.startX, self.endX, self.startY, self.endY)

	def area(self):
		"""Returns the area of a given box"""
		return self.width() * self.height()
	
	def width(self):
		return (self.endX - self.startX)

	def height(self):
		return (self.endY - self.startY)

	#@printRet
	def dist(self, other):
		"""Finds the shortest distance between the two boxes.
		Returns 0 if the boxes are overlapping, or if one box
		is inside another box. 
		"""
		if self.areInside(other):
			return 0

		if self.overlap(other):
			return 0
		
		# Cases when the tiles are laying parallel to each other
		# Projection across the x axis
		if self.startX <= other.startX <= self.endX or\
			self.startX <= other.endX <= self.endX or \
			other.startX <= self.startX <= other.endX or \
			other.startX <= self.endX <= other.endX:
			return min(abs(self.startY - other.endY), abs(self.endY - other.startY))

		# Projection across the y axis
		if self.startY <= other.startY <= self.endY or\
			self.startY <= other.endY <= self.endY or \
			other.startY <= self.startY <= other.endY or \
			other.startY <= self.endY <= other.endY:
			return min(abs(self.startX - other.endX), abs(self.endX - other.startX))
					
		# Last case is when the tiles are disjoint from each other
		else:		
			# Case 1: self is to the right of other
			if other.endX < self.startX:
				# Case 1.1: other is above self
				# Other is northwest of self
				if other.endY < other.startY:
					return Box.euclid(self.startX, other.endX, self.startY, other.endY)
				# Case 1.2: other is below self
				return Box.euclid(self.startX, other.endX, self.endY, other.startY)

			# Case 2: self is to the left of other
			else:
				# Case 2.1: other is above self
				if other.endY < self.startY:
					return Box.euclid(self.endX, other.startX, self.startY, other.endY)
				# Case 2.2: other is below self
				# Other is southeast of self
				return Box.euclid(self.endX, other.startX, self.endY, other.startY)
	
	@staticmethod
	def euclid(x1, x2, y1, y2):
		return sqrt( (x1 - x2)**2 + (y1 - y2)**2)


	def getContourRep(self):
		"""Obtains the numpy array representation of the box """
		vertex1 = [[self.startX, self.startY]]
		vertex2 = [[self.startX, self.endY]]
		vertex3 = [[self.endX, self.startY]]
		vertex4 = [[self.endX, self.endY]]
		vertices = [vertex1, vertex2, vertex3, vertex4]
		return convexHull(np.asarray(vertices, dtype = np.int32))
	
	def areInside(self, other):
		"""Returns true if and only if one rectangle is a subset of another"""
		otherInSelf = self.startX <= other.startX <= self.endX and \
			self.startX <= other.endX <= self.endX and\
			self.startY <= other.startY <= self.endY and\
			self.startY <= other.endY <= self.endY
		selfInOther = other.startX <= self.startX <= other.endX and\
			other.startX <= self.endX <=other.endX and\
			other.startY <= self.startY <= other.endY and\
			other.startY <= self.endY <= other.endY
		return otherInSelf or selfInOther
	
	def overlap(self, other):
		"""Returns true if the boxes are overlapping."""
		overlap = self.contains(other.startX, other.startY) or \
			self.contains(other.startX, other.endY) or \
			self.contains(other.endX, other.startY) or \
			self.contains(other.endX, other.endY)

		intersectY1 = self.startY <= other.startY <= self.endY and \
			self.startY <= other.endY <= self.endY and \
			(other.startX <= self.startX <= other.endX or \
			other.startX <= self.endX <= other.endX)

		intersectY2 = other.startY <= self.startY <= other.endY and \
			  other.startY <= self.endY <= other.endY and \
			  (self.startX <= other.startX <= self.endX or \
			   self.startX <= other.endX <= self.endX)

		intersectY = intersectY1 or intersectY2

		intersectX1 = self.startX <= other.startX <= self.endY and \
			self.startX <= other.endX <= self.endX and \
		    (other.startY <= self.startY <= other.endY or \
			other.startY <= self.endY <= other.endY)

		intersectX2 = other.startX <= self.startX <= other.endX and \
			other.startX <= self.endX <= other.endX and \
		    (self.startY <= other.startY <= self.endY or \
			self.startY <= other.endY <= self.endY)

		intersectX = intersectX1 or intersectX2

		return overlap or intersectX or intersectY


	def contains(self, x, y):
		"""Returns true if and only if the rectangle contains the point"""
		return self.startX <= x <= self.endX and self.startY <= y <= self.endY
