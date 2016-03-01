#!/usr/bin/env python2.7
import math
import random
import copy
def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def closerThumb(lPoint, rPoint, destination):
	leftDist = distance(lPoint,destination)
	rightDist = distance(rPoint,destination)
	if leftDist <= rightDist:
		return 'l'
	else:
		return 'r'

def update(thumb,destination):
	global totalDistance
	global leftPosition
	global rightPosition
	if thumb == 'right':
		# print distance(leftPosition,destination)
		totalDistance += distance(rightPosition,destination)
		rightPosition = destination
	elif thumb == 'left':
		# print distance(leftPosition,destination)
		totalDistance += distance(leftPosition,destination)
		leftPosition = destination

def keyboard(inputLetters, inputCoordinates):
	random.shuffle(inputLetters)
	random.shuffle(inputCoordinates)
	myKeyboard = {}
	for i in range(0,len(inputCoordinates)):
		myKeyboard[inputLetters[i]] = inputCoordinates[i]
	return myKeyboard

def mobileTest(inputText, theKeyboard):
	totalTransitions = len(inputText)
	global totalDistance

	for j in range(0,len(inputText)):
		nextLetter = inputText[j]
		nextPosition = theKeyboard[nextLetter]
		if nextPosition in rightOnly:
			# print "right to", nextLetter
			update('right',nextPosition)
			# print "dist", totalDistance
		elif theKeyboard[nextLetter] in leftOnly:
			# print "left to", nextLetter
			update('left',nextPosition)
			# print "dist", totalDistance
		else:
			if closerThumb(leftPosition,rightPosition,nextPosition) == 'r':
				# print "right to", nextLetter
				update('right',nextPosition)
				# print "dist", totalDistance
			elif closerThumb(leftPosition,rightPosition,nextPosition) == 'l':
				# print "left to", nextLetter
				update('left',nextPosition)
				# print "dist", totalDistance
	return (totalDistance/totalTransitions), theKeyboard,

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

def keyboardDisplay(keyDict):
	k = invertDict(keyDict)
	return '''
 _______ _______ _______ _______ _______ _______ _______ _______ _______ _______
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
                    |                   {27}                   |
                    |_______________________________________|
		'''.format(k['0, 3'], k['1, 3'], k['2, 3'], k['3, 3'], k['4, 3'], k['5, 3'], k['6, 3'], k['7, 3'], k['8, 3'], k['9, 3'], k['0.5, 2'], k['1.5, 2'], k['2.5, 2'], k['3.5, 2'], k['4.5, 2'], k['5.5, 2'], k['6.5, 2'], k['7.5, 2'], k['8.5, 2'], k['0, 0'], k['1.5, 1'], k['2.5, 1'], k['3.5, 1'], k['4.5, 1'], k['5.5, 1'], k['6.5, 1'], k['7.5, 1'], k['5.5, 0'])
if __name__ == '__main__':
	leftOnly = [
	[0,3],[1,3],[2,3],[3,3],[4,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1]]
	rightOnly = [
	[5,3],[6,3],[7,3],[8,3],[9,3],
	[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
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
	newcoord = []

	leftPosition = [3.5,2]
	rightPosition = [6.5,2]

	# theInput = 'With a little plumbing we can create a system that allows one module to directly ask for the interface object of another module without going through the global scope Our goal is a require function that when given a module name will load that modules file from disk or the Web depending on the platform we are running on and return the appropriate interface value'
	theInput = "The Quick Brown Fox"
	theInput = changeCapitals(theInput)

	best = 1.3
	bestDict = {}

	# for i in range(0,2000000):
	#found 1043, watch says 3:30
	solNumber = 1
	for i in range(0,1):
		totalDistance = 0
		# trialKeyboard = keyboard(letters,coordinates)
		trialKeyboard = {' ': [2.5, 2], '^': [7.5, 2], 'a': [0, 0], 'c': [3, 3], 'b': [7, 3], 'e': [0.5, 2], 'd': [6, 3], 'g': [5.5, 0], 'f': [8.5, 2], 'i': [4.5, 2], 'h': [1, 3], 'k': [6.5, 1], 'j': [5, 3], 'm': [4, 3], 'l': [3.5, 1], 'o': [8, 3], 'n': [2.5, 1], 'q': [4.5, 1], 'p': [5.5, 2], 's': [1.5, 1], 'r': [6.5, 2], 'u': [7.5, 1], 't': [0, 3], 'w': [2, 3], 'v': [1.5, 2], 'y': [5.5, 1], 'x': [3.5, 2], 'z': [9, 3]}
		answer = mobileTest(theInput, trialKeyboard)
		print answer
		answer = list(answer)
		if answer[0] < 1.3:
			best = answer[0]
			bestDict = copy.deepcopy(answer[1])
			print solNumber, best
			solNumber += 1
			with open("results2.txt", "a") as myfile:
				myfile.write(str(best))
				myfile.write('\n')
				myfile.write(str(bestDict))
				myfile.write(keyboardDisplay(bestDict))
				myfile.write('\n')
