#!/usr/bin/env python2.7
from __future__ import division
from wand.image import Image
import math
from random import shuffle
from random import uniform
from random import choice

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def makeKeyboardImage(thisDict, filename):
	keyNumberToCoordinates = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}
	letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','^','z','x','c','v','b','n','m',' ']
	if isinstance(thisDict['q'], int):
		newDict = {}
		for i in thisDict:
			newDict[i] = keyNumberToCoordinates[thisDict[i]]
		thisDict = newDict
	w = 1000
	h = 400
	with Image(width=w, height=h, background=None) as board:
		for i in letters:
			if i == ' ':
				name = '_.png'
			else:
				name = i+'.png'
			with Image(filename=name) as key:
				board.composite(key, left=int(thisDict[i][0]*100), top=(h-int(thisDict[i][1]*100))-100)
		board.save(filename=filename+'.png')

def makeStringImage(inputString, filename):#filename must include extension
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
	w = 1000
	h = 400
	with Image(width=w, height=h, background=None) as board:
		for i in range(len(inputString)):
			if inputString[i] == ' ':
				name = '_.png'
			else:
				name = inputString[i] + '.png'
			with Image(filename=name) as letter:
				board.composite(letter, left=int(coordinates[i][0]*100), top=(h-int(coordinates[i][1]*100))-100)
		board.save(filename = filename)

makeStringImage('vhtdzu^gcko aqrpeilwnbxmsfyj', 'STRINGTEST.png')

def midpoint(c1, c2):
	theMidpoint = [(c1[0]+c2[0])/2,(c1[1]+c2[1])/2]
	return theMidpoint

def randomModify(d):
	plusMinus = [-1,1]
	for i in d:
		y = uniform(0, 0.30)
		x = uniform(0, 0.30)
		d[i] = [d[i][0]+(y*choice(plusMinus)),d[i][1]+(x*choice(plusMinus))]
	return d

def averageKeyboard(dict1, dict2):
	keyNumberToCoordinates = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}
	letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','^','z','x','c','v','b','n','m',' ']

	if isinstance(dict1['q'], int):
		newDict = {}
		for i in dict1:
			newDict[i] = keyNumberToCoordinates[dict1[i]]
		dict1 = newDict
	if isinstance(dict2['q'], int):
		newDict = {}
		for i in dict2:
			newDict[i] = keyNumberToCoordinates[dict2[i]]
		dict2 = newDict

	meanDict = {}
	for i in letters:
		meanDict[i] = midpoint(dict1[i],dict2[i])
	return meanDict

def spreadKeys(d):
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],[5.5,0]]
	shuffle(coordinates)
	#shuffled to prevent repetitive bias
	for i in d:
		if d[i] in coordinates:
			coordinates.remove(d[i])
		else:
			lowestDistance = 100
			closestCoordinate = []
			for j in coordinates:
				if distance(d[i],j) < lowestDistance:
					lowestDistance = distance(d[i],j)
					closestCoordinate = j
			d[i] = closestCoordinate
			coordinates.remove(closestCoordinate)
	return d

def greedySpreadKeys(d):
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],[5.5,0]]
	letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','^','z','x','c','v','b','n','m',' ']
	shuffle(coordinates)
	dlist = {}
	for i in d:
		dlist[i] = [] 
		for l in coordinates:
			dlist[i] = dlist[i] + [[distance(l,d[i]),l,i]]
	for i in dlist:
		dlist[i].sort()
	finalDict = {}
	skip = []
	shuffle(letters)
	for p in range(len(letters)):
		closestValues = []
		for i in letters:
			#populating closest values
			for j in range(len(dlist)):#will return the lowest thing for every element in dlist 
				if dlist[i][j][1] in coordinates:
					closestValues.append(dlist[i][j])
					break
		minimum = min(closestValues)
		finalDict[minimum[2]] = minimum[1]
		coordinates.remove(minimum[1])
		letters.remove(minimum[2])
	return finalDict

# best  = {' ': 17, '^': 5, 'a': 13, 'c': 9, 'b': 15, 'e': 18, 'd': 26, 'g': 16, 'f': 21, 'i': 7, 'h': 4, 'k': 24, 'j': 25, 'm': 27, 'l': 22, 'o': 12, 'n': 3, 'q': 1, 'p': 19, 's': 23, 'r': 2, 'u': 11, 't': 8, 'w': 14, 'v': 10, 'y': 6, 'x': 28, 'z': 20}
# theoretical = {' ': 17, '^': 5, 'a': 16, 'c': 8, 'b': 9, 'e': 13, 'd': 14, 'g': 23, 'f': 27, 'i': 3, 'h': 21, 'k': 24, 'j': 1, 'm': 25, 'l': 7, 'o': 12, 'n': 26, 'q': 28, 'p': 15, 's': 2, 'r': 22, 'u': 4, 't': 18, 'w': 11, 'v': 19, 'y': 6, 'x': 20, 'z': 10}
# x = averageKeyboard(best,theoretical)

# # z = randomModify(x)
# # makeKeyboardImage(z,'KEYBOARD')
# y = greedySpreadKeys(x)
# # for i in y:
# # 	print y[i]
# makeKeyboardImage(y,'GREEDY')
# makeKeyboardImage(best,'BEST')

# if __name__ == '__main__':
# 	minimum = {' ': 17, '^': 5, 'a': 13, 'c': 9, 'b': 15, 'e': 18, 'd': 26, 'g': 16, 'f': 21, 'i': 7, 'h': 4, 'k': 24, 'j': 25, 'm': 27, 'l': 22, 'o': 12, 'n': 3, 'q': 1, 'p': 19, 's': 23, 'r': 2, 'u': 11, 't': 8, 'w': 14, 'v': 10, 'y': 6, 'x': 28, 'z': 20}
# 	makeKeyboardImage(minimum)
#  		# for i in letters:
# 	#	 print ("convert -size 100x100 xc:transparent '{0}.png'".format(i))
# 	#	 print ("convert '{0}.png' -fill white -stroke black -strokewidth 3 -draw 'rectangle 3,3 96,96' {0}.png -gravity Center -fill black -stroke black -pointsize 70 -annotate 0 '{0}' {0}.png".format(i))
