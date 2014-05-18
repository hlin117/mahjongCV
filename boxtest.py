#!/usr/bin/python
from box import Box
from colorama import *


def assertEqs(x, y):
	if x != y:
		print Fore.RED + "Unexpected output: {0}".format(x) + Fore.RESET

	else:
		print Fore.GREEN + "Passed test" + Fore.RESET

def assertSymmetry(box1, box):
	if box1.dist(box2) != box2.dist(box1):
		print Fore.RED + "Distances aren't symmetric" + Fore.RESET

	else:
		print Fore.GREEN + "Passed symmetry test" + Fore.RESET
	

def reset(* boxes):
	for box in boxes:
		box = None
"""
# Tests the box module
box1 = Box(10, 10, 5, 5)
box2 = Box(0, 0, 5, 5)
box3 = Box(1, 1, 1, 1)

print box1
print box2

distance = box1.dist(box2)
distance = box2.dist(box1)
assertEqs(box2.dist(box3),  0)
assertSymmetry(box1, box2)
assertSymmetry(box2, box3)
assertSymmetry(box1, box3)

box1 = Box(1, 1, 2, 2)
print box1
box2 = Box(2, 2, 2, 2)
print box2

assertEqs(box1.dist(box2), 0)
assertSymmetry(box1, box2)

box1 = Box(0, 0, 2, 4)
box2 = Box(1, 1, 1, 1)
box3 = Box(1, 3, 3, 4)
newBox = Box.meld(box1, box2, box3)
print newBox

box1 = Box(0, 0, 2, 3)
box2 = Box(4, 0, 1, 4)
assertEqs(box1.dist(box2), 2)
assertSymmetry(box1, box2)

box3 = Box(1, 2, 3, 3)
newBox = Box.meld(box1, box2, box3)
print newBox

box1 = Box(318, 159, 373 - 318, 184 - 159)
box2 = Box(330, 100, 363-330, 147-100)
print box1.dist(box2)
print box2.dist(box1)
assertSymmetry(box1, box2)
"""

box1 = Box(168, 120, 235 - 163, 148 - 120) # 21
box2 = Box(166, 77, 212 - 166, 111 - 77) # 24
print box1.dist(box2)
assertSymmetry(box1, box2)


box1 = Box(46, 58, 120 - 46, 160 - 58)
box2 = Box(163, 120, 235 - 163, 148 - 120)
print box1.dist(box2)
assertSymmetry(box1, box2)


box1 = Box(46, 58, 210 - 46, 160 - 58)
box2 = Box(40, 60, 91 - 40, 111 - 60)
print box1.dist(box2)
print box2.dist(box1)
assertSymmetry(box1, box2)

box1 = Box(487, 367, 523 - 487, 374 - 367)
box2 = Box(444, 353, 480 - 444, 359 - 353)
print box1.dist(box2)
print box2.dist(box1)
assertSymmetry(box1, box2)

print "\nAnother test..."
box1 = Box(318, 149, 322 - 318, 172 - 149)
box2 = Box(307, 173, 312 - 307, 197 - 173)
print box1.dist(box2)
print box2.dist(box1)
assertSymmetry(box1, box2)

print "\nOne more test..."
box1 = Box(250, 150, 260 - 250, 164 - 150)
box2 = Box(262, 167, 275 - 262, 184 - 167)
assertSymmetry(box1, box2)
