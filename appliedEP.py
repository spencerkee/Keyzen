#!/usr/bin/python2.7
# -*- coding: utf-8 -*-1

import random
# import compiledGradient
import numpy
import math
#keyboard format is qwertyuiopasdfghjkl↑zxcvbnm←
#← LEFT ARROW = backspace
#↑ UP ARROW = shift
#■ BLACK SQUARE = mod key (123)
# backspaceKey = '←'
# shiftKey = '↑'
# modKey = '■'

# Step 1: Create a pool containing p randomly-generated keyboard layouts.
# Step 2: Score each keyboard according to a fitness function and sort the keyboards by score.
# Step 3: Randomly delete half of the pool (giving preference to keyboards with lower fitness) and create a copy of each remaining keyboard.
# Step 4: Mutate the copies by randomly swapping the positions of two keys m times.
# Step 5: Repeat steps 2-4 until the best keyboard in the pool has not changed for b rounds.
# Step 6: Place this best k keyboards in pool O and sort each keyboard in O by score.
# Step 7: Repeat steps 2-6 until O contains o layouts.
# Step 8: Repeat steps 2-4 using pool O until the best keyboard in the pool has not changed for q rounds.

letterString = 'qwertyuiopasdfghjkl^zxcvbnm '

def distance(p0, p1):#simple distance formula
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def createNKeyboards(n):#generates n keyboards in the form of scrambled letterString
	returnList = []
	for i in range(n+1):
		returnList.append(''.join(random.sample(letterString,len(letterString))))
	return returnList

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

def stringFitnesses(inputText, keyboardStrings):
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
	sameLetterCost = 0
	inputText = changeCapitals(inputText)
	totalTransitions = len(inputText)
	distanceMatrix = numpy.zeros(shape=(len(letterString),len(letterString)))
	leftOnly = [0,1,2,3,4,10,11,12,13,19,20,21,22]
	rightOnly = [5,6,7,8,9,15,16,17,18,24,25,26,27]
	letterNum = {}
	numCoord = {}
	for i in range(len(letterString)):
		letterNum[letterString[i]] = i
	returnList = []
	for individualKeyboard in keyboardStrings:
		totalDistance = 0
		leftPosition = 14
		rightPosition = 17
		# myString.index('s')
		for letter in inputText:
			print 'letter', letter
			if letterNum[letter] == leftPosition or letterNum[letter] == rightPosition:
				totalDistance += sameLetterCost
			elif letterNum[letter] != leftPosition and letterNum[letter] != rightPosition:
				if letterNum[letter] in rightOnly:
					print 'right'
					if distanceMatrix[rightPosition, letterNum[letter]] == 0.0:
						print 'zero'
						distanceMatrix[rightPosition, letterNum[letter]] = distance(coordinates[rightPosition], coordinates[letterNum[letter]])
						distanceMatrix[rightPosition, letterNum[letter]] = distanceMatrix[letterNum[letter], coordinates[rightPosition]
					totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
					rightPosition = letterNum[letter]
				elif letterNum[letter] in leftOnly:
					print 'left'
					if distanceMatrix[leftPosition, letterNum[letter]] == 0.0:
						print 'zero'
						distanceMatrix[leftPosition, letterNum[letter]] = distance(coordinates[leftPosition], coordinates[letterNum[letter]])
						distanceMatrix[leftPosition, letterNum[letter]] = distanceMatrix[letterNum[letter], leftPosition]
					totalDistance += distanceMatrix[leftPosition, letterNum[letter]]
					leftPosition = letterNum[letter]
				else: 
					if distanceMatrix[rightPosition, letterNum[letter]] == 0.0:
						distanceMatrix[rightPosition, letterNum[letter]] = distance(coordinates[rightPosition], coordinates[letterNum[letter]])
						distanceMatrix[rightPosition, letterNum[letter]] = distanceMatrix[letterNum[letter], rightPosition]
					if distanceMatrix[leftPosition, letterNum[letter]] == 0.0:
						distanceMatrix[leftPosition, letterNum[letter]] = distance(coordinates[leftPosition], coordinates[letterNum[letter]])
						distanceMatrix[leftPosition, letterNum[letter]] = distanceMatrix[letterNum[letter], leftPosition]
					if distanceMatrix[rightPosition, letterNum[letter]] <= distanceMatrix[leftPosition, letterNum[letter]]:
						totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
						rightPosition = letterNum[letter]
					else:
						totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
						rightPosition = letterNum[letter]
		returnList.append((totalDistance/totalTransitions))
	return returnList

theInput = "The Quick Brown Fox"
# theInput = 'With a little plumbing we can create a system that allows one module to directly ask for the interface object of another module without going through the global scope Our goal is a require function that when given a module name will load that modules file from disk or the Web depending on the platform we are running on and return the appropriate interface value'
print stringFitnesses(theInput, createNKeyboards(1))