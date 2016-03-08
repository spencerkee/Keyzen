#!/usr/bin/env python2.7
import math
import random
import copy
import numpy
import itertools
import pickle

def keyboardDisplay(keyDict):
	k = invertDict(keyDict)
	print ''
	# print k
	return ''' _______ _______ _______ _______ _______ _______ _______ _______ _______ _______
|       |       |       |       |       |       |       |       |       |       |
|   {0}   |   {1}   |   {2}   |   {3}   |   {4}   |   {5}   |   {6}   |   {7}   |   {8}   |   {9}   |
|_______|_______|_______|_______|_______|_______|_______|_______|_______|_______|
	 _______ _______ _______ _______ _______ _______ _______ _______ _______
	|       |       |       |       |       |       |       |       |       |
	|   {10}   |   {11}   |   {12}   |   {13}   |   {14}   |   {15}   |   {16}   |   {17}   |   {18}   |
	|_______|_______|_______|_______|_______|_______|_______|_______|_______|
	 _______ _______ _______ _______ _______ _______ _______ _______
	|       |       |       |       |       |       |       |       |
	|   {19}   |   {20}   |   {21}   |   {22}   |   {23}   |   {24}   |   {25}   |   {26}   |
	|_______|_______|_______|_______|_______|_______|_______|_______|
                         _______________________________________
                        |                                       |
                        |                           {27}           |
                        |_______________________________________|
		'''.format(k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9], k[10], k[11], k[12], k[13], k[14], k[15], k[16], k[17], k[18], k[19], k[20], k[21], k[22], k[23], k[24], k[25], k[26], k[27], k[28])

def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def closerThumb(lPoint, rPoint, destination):#trying the distanceMatrix and catching it might be faster
	global distanceMatrix
	global numCoord
	if distanceMatrix[lPoint,destination] == 0.0:
		distanceMatrix[lPoint,destination] == distance(numCoord[lPoint],numCoord[destination])
		distanceMatrix[destination, lPoint] = distanceMatrix[lPoint, destination]
		leftDist = distanceMatrix[lPoint,destination]
	else:
		leftDist = distanceMatrix[lPoint,destination]
	if distanceMatrix[rPoint,destination] == 0.0:
		distanceMatrix[rPoint,destination] == distance(numCoord[rPoint],numCoord[destination])
		distanceMatrix[destination,rPoint] = distanceMatrix[rPoint,destination]
		rightDist = distanceMatrix[rPoint,destination]
	else:
		rightDist = distanceMatrix[rPoint,destination]
	if leftDist <= rightDist:
		return 'l'
	else:
		return 'r'

def convertToCoord(string, localDict):
	coordList = []
	for i in range(0,len(string)):
		coordList.append(localDict[string[i]])
	return coordList

def invertDict(thisDict):
	newDict = {}
	for k in thisDict:
		newDict[thisDict[k]] = k
	return newDict

def changeCapitals(myInput):
	firstMarker = 0
	stringList = []
	for i in range(0,len(myInput)):
		if myInput[i].isupper() == True:
			stringList.append(myInput[firstMarker:-(len(myInput)-i)])
			stringList.append('^{0}'.format(myInput[i].lower()))
			firstMarker = i+1
	stringList.append(myInput[firstMarker:len(myInput)])
	return "".join(stringList)

def mobileFitness(inputText, letterNumberDict, numberCoordDict):

	totalTransitions = len(inputText)
	global distanceMatrix
	global totalDistance
	global rightPosition
	global leftPosition
	totalDistance = 0

	for j in range(0,len(inputText)):
		nextLetter = inputText[j]
		nextKeynumber = letterNumberDict[nextLetter]
		if nextKeynumber != leftPosition and nextKeynumber != rightPosition:
			if nextKeynumber in rightOnly and nextKeynumber:
				update('right', nextKeynumber)
			elif nextKeynumber in leftOnly and nextKeynumber:
				update('left', nextKeynumber)
			else:
				if closerThumb(leftPosition,rightPosition,nextKeynumber) == 'r':
					update('right',nextKeynumber)
				else:
					update('left',nextKeynumber)
	return totalDistance/totalTransitions

def update(thumb,destination):
#if something is not in right or left only than distance is called twice, for closer thumb and update
	global totalDistance
	global leftPosition
	global rightPosition
	global distanceMatrix
	global numCoord

	if thumb == 'right':
		if distanceMatrix[rightPosition, destination] == 0.0:
			distanceMatrix[rightPosition, destination] = distance(numCoord[rightPosition], numCoord[destination])
			distanceMatrix[destination, rightPosition] = distanceMatrix[rightPosition, destination]
		totalDistance += distanceMatrix[rightPosition, destination]
		rightPosition = destination
	elif thumb == 'left':
		if distanceMatrix[leftPosition, destination] == 0.0:
			distanceMatrix[leftPosition, destination] = distance(numCoord[leftPosition], numCoord[destination])
			distanceMatrix[destination, leftPosition] = distanceMatrix[leftPosition, destination]
		totalDistance += distanceMatrix[leftPosition, destination]
		leftPosition = destination


def letterToNumber(inputLetters):
	numbersForKeys = range(1,len(inputLetters)+1)
	if len(inputLetters) != len(numbersForKeys):
		print "l2n problem"
	random.shuffle(numbersForKeys)
	myKeyboard = {}
	for i in range(0,len(inputLetters)):
		myKeyboard[inputLetters[i]] = numbersForKeys[i]
	return myKeyboard

def numberToCoord(keyCoords):
	keyNumbers = range(1,29)
	ntcDict = {}
	if len(keyNumbers) != len(keyCoords):
		print "n2c not equal"
	for i in range(0, len(keyNumbers)):
		ntcDict[keyNumbers[i]] = keyCoords[i]
	return ntcDict

def swapKey(d,k1,k2):
	d[k1], d[k2] = d[k2], d[k1]
	return d

if __name__ == '__main__':
	leftOnly = [1,2,3,4,5,11,12,13,14,20,21,22,23]
	rightOnly = [6,7,8,9,10,16,17,18,19,25,26,27,28]
	letters = [
	'q','w','e','r','t','y','u','i','o','p',
	'a','s','d','f','g','h','j','k','l',
	'^','z','x','c','v','b','n','m',
	' ']
	coordinates = [
	[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
	leftPosition = 14
	rightPosition = 17

	theInput = 'With a little plumbing we can create a system that allows one module to directly ask for the interface object of another module without going through the global scope Our goal is a require function that when given a module name will load that modules file from disk or the Web depending on the platform we are running on and return the appropriate interface value'
	lowerInput = changeCapitals(theInput)

	numCoord = numberToCoord(coordinates)
	distanceMatrix = numpy.zeros(shape=(29,29))
	letterNum = letterToNumber(letters)

	totalDistance = 0
	previousBest = mobileFitness(lowerInput, letterNum, numCoord)
	testBest = 100
	possibleSwaps = itertools.combinations(letterNum, 2)
	possibleSwaps = [list(i) for i in possibleSwaps]
	# print letterNum
	results = []
	for thing in range(500):
		print thing
		letterNum = letterToNumber(letters)
		previousBest = 100
		while True:
			random.shuffle(possibleSwaps)
			index = 0
			while index < len(possibleSwaps):
				letterNum = swapKey(letterNum, possibleSwaps[index][0],possibleSwaps[index][1])
				testBest = mobileFitness(lowerInput, letterNum, numCoord)
				if testBest >= previousBest:
					letterNum = swapKey(letterNum, possibleSwaps[index][0], possibleSwaps[index][1])
				else:
					previousBest = testBest
					break
				index += 1
			if index == len(possibleSwaps):
				break
		with open("pickleTest", "a") as myfile:
			pickle.dump([previousBest,letterNum], myfile)
