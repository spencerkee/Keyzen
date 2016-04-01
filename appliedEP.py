#!/usr/bin/python2.7
# -*- coding: utf-8 -*-1
from __future__ import division
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

theInput = '''Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.
'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)
Down, down, down. Would the fall never come to an end! 'I wonder how many miles I've fallen by this time?' she said aloud. 'I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think' (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) 'yes, that's about the right distancebut then I wonder what Latitude or Longitude I've got to?' (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)'''



letterString = 'qwertyuiopasdfghjkl^zxcvbnm '

def distance(p0, p1):#simple distance formula
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def createNKeyboards(n):#generates n keyboards in the form of scrambled letterString
	returnList = []
	for i in range(n):
		returnList.append(''.join(random.sample(letterString,len(letterString))))
	return returnList

def processText(myInput):#removes symbols (inefficiently) and changes capitals into lowercase letters prepended with ^. could be improved with exceptions
    symbols = ['.',',','?','!','"',"'",'\n',')','(',':',';', '-']
    for i in symbols:
        myInput=myInput.replace(i,'')
    firstMarker = 0
    stringList = []
    for i in range(0,len(myInput)):
        if myInput[i].isupper() == True:
            stringList.append(myInput[firstMarker:-(len(myInput)-i)])
            stringList.append('^{0}'.format(myInput[i].lower()))
            firstMarker = i+1
    stringList.append(myInput[firstMarker:len(myInput)])
    return "".join(stringList)

def stringFitnesses(inputText, keyboardStrings):#returns the list of fitnesses of a list of keyboards
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
	sameLetterCost = 0
	inputText = processText(inputText)
	totalTransitions = len(inputText)
	distanceMatrix = numpy.zeros(shape=(len(letterString),len(letterString)))
	for i in range(len(coordinates)):
		for j in range(len(coordinates)):
			distanceMatrix[i][j] = distance(coordinates[i],coordinates[j])
			distanceMatrix[j][i] = distanceMatrix[i][j]
	leftOnly = [0,1,2,3,4,10,11,12,13,19,20,21,22]
	rightOnly = [5,6,7,8,9,15,16,17,18,24,25,26,27]

	returnList = []
	for individualKeyboard in keyboardStrings:
		letterNum = {}
		for i in range(len(letterString)):
			letterNum[individualKeyboard[i]] = i
		totalDistance = 0
		leftPosition = 13
		rightPosition = 16
		# myString.index('s')
		for letter in inputText:
			# print letter
			if letterNum[letter] == leftPosition or letterNum[letter] == rightPosition:
				totalDistance += sameLetterCost
			elif letterNum[letter] != leftPosition and letterNum[letter] != rightPosition:
				if letterNum[letter] in rightOnly:
					totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
					# print distanceMatrix[rightPosition, letterNum[letter]]
					rightPosition = letterNum[letter]
				elif letterNum[letter] in leftOnly:
					totalDistance += distanceMatrix[leftPosition, letterNum[letter]]
					# print distanceMatrix[leftPosition, letterNum[letter]]
					leftPosition = letterNum[letter]
				else:
					if distanceMatrix[rightPosition, letterNum[letter]] <= distanceMatrix[leftPosition, letterNum[letter]]:
						totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
						# print distanceMatrix[rightPosition, letterNum[letter]]
						rightPosition = letterNum[letter]
					else:
						totalDistance += distanceMatrix[leftPosition, letterNum[letter]]
						# print distanceMatrix[leftPosition, letterNum[letter]]
						leftPosition = letterNum[letter]
		returnList.append((totalDistance/totalTransitions))
	return returnList

#this can't be good because 1% of 50 is nothing
def mutateKeyboards(keyboardList, mutationPercent, swapNumber):#if the percent is 40, and there are 2 keyboards, no mutations are made
	returnList = []
	swapIndicies = range(len(keyboardList))
	random.shuffle(swapIndicies)
	swapIndicies = swapIndicies[0:int(len(keyboardList)*(mutationPercent/100))]
	for i in swapIndicies:
		lst = list(keyboardList[i])
		for l in range(swapNumber):
			j = random.randint(0,len(keyboardList[i])-1)
			k = random.randint(0,len(keyboardList[i])-1)
			lst[j], lst[k] = lst[k], lst[j]
		keyboardList[i] = (''.join(lst))
	return keyboardList

def singlePointCrossover(parent1, parent2):
	crossoverPoint = random.randint(0,len(parent1)-1)
	newKeyboard = parent1[:crossoverPoint]
	addLetters = []
	for i in parent2:
		if i not in newKeyboard:
			addLetters.append(i)
	newKeyboard = newKeyboard + ''.join(addLetters)
	return newKeyboard

def rouletteSelection(inputFitnessList):#higher chance of removing large (bad) fitnesses. Removes 50%, then duplicates remaining fitnesses
	inputFitnessList = list(inputFitnessList)
	numberDeleted = 0
	goal = int(len(inputFitnessList)/2)
	while numberDeleted < goal:
		max = sum(inputFitnessList)
		pick = random.uniform(0,max)
		currentValue = 0
		index = 0
		for i in inputFitnessList:
			currentValue += i
			if currentValue > pick:
				break
			index+=1
		inputFitnessList.pop(index)
		numberDeleted+=1
	inputFitnessList = inputFitnessList + inputFitnessList
	return inputFitnessList

def eliteRouletteSelection(inputFitnessList, elitePercent):
	#the lowest elitePercent are saved, then half of the remaining are roulette deleted, then random selections are added until the returnList is the same length as it originally was
	inputFitnessList = list(inputFitnessList)
	originalLength = len(inputFitnessList)
	inputFitnessList.sort()
	splitPoint = int(len(inputFitnessList)*(elitePercent/100))
	eliteSelection = inputFitnessList[0:splitPoint]
	remainingFitnesses = inputFitnessList[splitPoint:len(inputFitnessList)]

	numberDeleted = 0
	goal = int(len(remainingFitnesses)/2)
	while numberDeleted < goal:
		max = sum(remainingFitnesses)
		pick = random.uniform(0,max)
		currentValue = 0
		index = 0
		for i in remainingFitnesses:
			currentValue += i
			if currentValue > pick:
				break
			index+=1
		remainingFitnesses.pop(index)
		numberDeleted+=1
	returnList = eliteSelection + remainingFitnesses
	random.shuffle(returnList)#should probably be random pick
	returnList = returnList + returnList[0:originalLength-len(returnList)]
	return returnList

#currently will never end using allSame. Should maybe try something based on the average or the best keyboard not changing for a while
def mateAndMutate(fitnessList, selectedList, keyboardList):#without mutation there are some nice ones
	keyboardIndicies = []
	for i in range(int(len(selectedList)/2)):
		keyboardIndicies.append(fitnessList.index(selectedList[i]))
	thisPopulation = []
	for i in keyboardIndicies:
		thisPopulation.append(keyboardList[i])
	thisPopulation = thisPopulation + thisPopulation
	random.shuffle(thisPopulation)
	nextGeneration = []
	for i in range(int(len(thisPopulation)/2)):#should parents have 2 children?
		j = i + int(len(thisPopulation)/2)
		nextGeneration.append(singlePointCrossover(thisPopulation[i],thisPopulation[j]))
	# nextGeneration = mutateKeyboards(nextGeneration, 10, 1)
	return nextGeneration + nextGeneration

def allSame(lst):
	firstValue = lst[0]
	for i in lst:
		if i != firstValue:
			return False
	return True

newPopulation= createNKeyboards(50)
for i in range(300):
	if allSame(newPopulation):
		break
	fitnesses = stringFitnesses(theInput, newPopulation)
	avg = sum(fitnesses)/len(fitnesses)
	minIndex = fitnesses.index(min(fitnesses))
	print 'average', avg, min(fitnesses),newPopulation[minIndex], i
	# print 'fitnesses', fitnesses
	selected = eliteRouletteSelection(fitnesses, 5)
	# print 'selected', selected
	newPopulation = mateAndMutate(fitnesses, selected,newPopulation)
	# print 'newPopulation', newPopulation
print newPopulation[0]








#if the last 5 values are the same, exit
#converged a35fter 128, 118, 1
#50 keys 99, 94, 121, 113, 52, 119