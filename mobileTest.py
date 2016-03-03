#!/usr/bin/env python2.7
import math
import random
import copy
import numpy

def keyboardDisplay(keyDict):
	k = invertDict(keyDict)
	return '''
 _______ _______ _______ _______ _______ _______ _______ _______ _______ _______
|	   |	   |	   |	   |	   |	   |	   |	   |	   |	   |
|   {0}   |   {1}   |   {2}   |   {3}   |   {4}   |   {5}   |   {6}   |   {7}   |   {8}   |   {9}   |
|_______|_______|_______|_______|_______|_______|_______|_______|_______|_______|
	 _______ _______ _______ _______ _______ _______ _______ _______ _______
	|	   |	   |	   |	   |	   |	   |	   |	   |	   |
	|   {10}   |   {11}   |   {12}   |   {13}   |   {14}   |   {15}   |   {16}   |   {17}   |   {18}   |
	|_______|_______|_______|_______|_______|_______|_______|_______|_______|
	 _______ _______ _______ _______ _______ _______ _______ _______
	|	   |	   |	   |	   |	   |	   |	   |	   |
	|   {19}   |   {20}   |   {21}   |   {22}   |   {23}   |   {24}   |   {25}   |   {26}   |
	|_______|_______|_______|_______|_______|_______|_______|_______|
					 _______________________________________
					|									   |
					|				   {27}				   |
					|_______________________________________|
		'''.format(k['0, 3'], k['1, 3'], k['2, 3'], k['3, 3'], k['4, 3'], k['5, 3'], k['6, 3'], k['7, 3'], k['8, 3'], k['9, 3'], k['0.5, 2'], k['1.5, 2'], k['2.5, 2'], k['3.5, 2'], k['4.5, 2'], k['5.5, 2'], k['6.5, 2'], k['7.5, 2'], k['8.5, 2'], k['0, 0'], k['1.5, 1'], k['2.5, 1'], k['3.5, 1'], k['4.5, 1'], k['5.5, 1'], k['6.5, 1'], k['7.5, 1'], k['5.5, 0'])

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
		newDict[str(thisDict[k])[1:-1]] = k
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

def mobileTest(inputText, letterNumberDict, numberCoordDict):

	totalTransitions = len(inputText)
	global distanceMatrix
	global totalDistance
	global rightPosition
	global leftPosition

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

def update(thumb,destination): #weakness of this is that az za are both calculated
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

if __name__ == '__main__':
	# q1, w2, e3, r4, t5, y6, u7, i8, o9, p10,
	# a11, s12, d13, f14, g15, h16, j17, k18, l19,
	# ^20, z21, x22, c23, v24, b25, n26, m27,
	#_28
	leftOnly = [
	1,2,3,4,5,
	11,12,13,14,
	20,21,22,23]
	rightOnly = [
	6,7,8,9,10,
	16,17,18,19,
	25,26,27,
	28]
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

	best = 1.55
	bestDict = {}

	solNumber = 0
	checkValue = 1.5
	#can test roughly 1100 per second
	answerString = ''
	distanceMatrix = numpy.zeros(shape=(29,29))
	for i in range(0,50000):
		letterNum = letterToNumber(letters)
		numCoord = numberToCoord(coordinates)
		totalDistance = 0
		answer = mobileTest(lowerInput, letterNum, numCoord)
		if answer < checkValue:
			answerString = answerString + str(answer) + ' ' + str(letterNum) + '\n'
			solNumber += 1
	with open("results3.txt", "a") as myfile:
		myfile.write(str(answerString))
	print distanceMatrix
	print solNumber
