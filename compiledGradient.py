#!/usr/bin/env python2.7
from __future__ import division
import collections
import copy
import itertools
import math
import numpy
import pickle
import random


def keyboardDisplay(keyDict):
    k = invertDict(keyDict)
    print ''
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
                        |                       {27}               |
                        |_______________________________________|
        '''.format(k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9], k[10], k[11], k[12], k[13], k[14], k[15], k[16], k[17], k[18], k[19], k[20], k[21], k[22], k[23], k[24], k[25], k[26], k[27], k[28])

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def closerThumb(lPoint, rPoint, destination):#trying the distanceMatrix and catching it might be faster
    global distanceMatrix
    localNumCoord = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}
    if distanceMatrix[lPoint,destination] == 0.0:
        distanceMatrix[lPoint,destination] == distance(localNumCoord[lPoint],localNumCoord[destination])
        distanceMatrix[destination, lPoint] = distanceMatrix[lPoint, destination]
        leftDist = distanceMatrix[lPoint,destination]
    else:
        leftDist = distanceMatrix[lPoint,destination]
    if distanceMatrix[rPoint,destination] == 0.0:
        distanceMatrix[rPoint,destination] == distance(localNumCoord[rPoint],localNumCoord[destination])
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

def mobileFitness(inputText, letterNumberDict):

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
    localNumCoord = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}

    if thumb == 'right':
        if distanceMatrix[rightPosition, destination] == 0.0:
            distanceMatrix[rightPosition, destination] = distance(localNumCoord[rightPosition], localNumCoord[destination])
            distanceMatrix[destination, rightPosition] = distanceMatrix[rightPosition, destination]
        totalDistance += distanceMatrix[rightPosition, destination]
        rightPosition = destination
    elif thumb == 'left':
        if distanceMatrix[leftPosition, destination] == 0.0:
            distanceMatrix[leftPosition, destination] = distance(localNumCoord[leftPosition], localNumCoord[destination])
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

def randomGradient(number, filename):
    for keyboardNumber in range(number):
        print str(keyboardNumber + 1) + '/' + str(number)
        letterNum = letterToNumber(letters)
        previousBest = 100
        while True:
            random.shuffle(possibleSwaps)
            index = 0
            while index < len(possibleSwaps):
                letterNum = swapKey(letterNum, possibleSwaps[index][0],possibleSwaps[index][1])
                testBest = mobileFitness(lowerInput, letterNum)
                if testBest >= previousBest:
                    letterNum = swapKey(letterNum, possibleSwaps[index][0], possibleSwaps[index][1])
                else:
                    previousBest = testBest
                    break
                index += 1
            if index == len(possibleSwaps):
                break
        with open(filename, "a") as myfile:
            pickle.dump([previousBest,letterNum], myfile)

def most_common(lst):
    return max(set(lst), key=lst.count)

def makeKeyboard(string):
    if len(string) != 28:
        return False
    stringList = list(string)
    returnDict = {}
    index = 1
    for j in stringList:
        returnDict[j] = index
        index += 1
    return returnDict

def extractPickles(filename):
    lists = []
    infile = open(filename, 'r')
    index = 0
    while 1:
        try:
            lists.append([pickle.load(infile),index])
        except (EOFError):
            break
        index += 1
    infile.close()
    return lists

def getMinKeyboard(filename):
    pickledResults = extractPickles(filename)
    return min(pickledResults)[0]

def duplicatesExist(results):
    resultsNum = len(results)
    results2 = [dict(t) for t in set([tuple(d.items()) for d in results])]
    if len(results2) < resultsNum:
        print "DUPLICATES EXIST"
    else:
        print "NO DUPliCATES"

def lettersOccurWhere(results): #create dictionary with letters for keys and list of tuples in the form (keyNumber, numOccurances)
    letterOccurances = {}
    letters = [
    'q','w','e','r','t','y','u','i','o','p',
    'a','s','d','f','g','h','j','k','l',
    '^','z','x','c','v','b','n','m',
    ' ']
    dupe = []
    for i in letters:
        letterOccurances[i] = []
    for j in results:
        dupe.append(j[0])
        for key in j[0][1]:
            letterOccurances[key] = letterOccurances[key] + [j[0][1][key]]
    fixedLO = {}
    for k in letterOccurances:
        counter=collections.Counter(letterOccurances[k])
        fixedLO[k] = counter.most_common(28)
    return fixedLO

def resultsTraverser(filename):#produces dictionary for every letter in the form ['s', 10.3, 12] letter, percent of keyboards it occurs in, keyNumber
    lists = extractPickles('pickleTest')
    resultsNum = len(lists)
    print "There are", resultsNum, "pickled keyboards"
    lettersAreHere = lettersOccurWhere(lists)
    freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
    qwer = {' ': 28, '^': 20, 'a': 11, 'c': 23, 'b': 25, 'e': 3, 'd': 13, 'g': 15, 'f': 14, 'i': 8, 'h': 16, 'k': 18, 'j': 17, 'm': 27, 'l': 19, 'o': 9, 'n': 26, 'q': 1, 'p': 10, 's': 12, 'r': 4, 'u': 7, 't': 5, 'w': 2, 'v': 24, 'y': 6, 'x': 22, 'z': 21}
    qwer = invertDict(qwer)
    #converts from lettersAreHere['a'] = [(12, 174), (13, 173), (17, 165), (16, 145), (18, 133), (3, 122), (26, 111), (14, 108), (22, 101), (8, 90), (7, 69), (4, 57), (25, 45), (27, 41), (21, 37), (2, 24), (11, 18), (9, 17), (23, 17), (15, 15), (19, 8), (24, 7), (5, 5), (6, 3), (1, 1), (28, 1)]
    #to lettersAreHere['a'] = ['a', ['s', 10.3, 12], ['d', 10.3, 13], ['j', 9.8, 17], ['h', 8.6, 16], ['k', 7.9, 18], ['e', 7.2, 3], ['n', 6.6, 26], ['f', 6.4, 14], ['x', 6.0, 22], ['i', 5.3, 8], ['u', 4.1, 7], ['r', 3.4, 4], ['b', 2.7, 25], ['m', 2.4, 27], ['z', 2.2, 21], ['w', 1.4, 2], ['a', 1.1, 11], ['o', 1.0, 9], ['c', 1.0, 23], ['g', 0.9, 15], ['l', 0.5, 19], ['v', 0.4, 24], ['t', 0.3, 5], ['y', 0.2, 6], ['q', 0.1, 1], [' ', 0.1, 28]]
    #['s', 10.3, 12] is letter, percent of keyboards it occurs in, keyNumber
    for l in lettersAreHere:
        line = [l]
        for y in lettersAreHere[l]:
            line.append([qwer[y[0]], round((y[1]/resultsNum)*100,1), y[0]])
        lettersAreHere[l] = line
    return lettersAreHere

def returnStrongestLetterPlacements(percentOccuranceDict):#returns list of keys that strongly tend to one position
    freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
    strongestOccuringLetters = []
    for p in freqSortedLetters:
        strongestOccuringLetters.append([lettersAreHere[p][1][1], lettersAreHere[p][0]])
    strongestOccuringLetters.sort(reverse = True)
    return strongestOccuringLetters

def strongestKeyboard(occuranceDict,presetKeyNum):#greedy algorithm that itereates over freqSortedLetters and places letters in their strongest position that isn't already filled
    freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
    strongestOccuringLetters = returnStrongestLetterPlacements(lettersAreHere)[:presetKeyNum]
    for i in strongestOccuringLetters:
        freqSortedLetters.remove(i[1])
    prependLetters = []
    for i in strongestOccuringLetters:
        prependLetters.append(i[1])
    freqSortedLetters = prependLetters + freqSortedLetters
    newDict = {}
    occupiedPositions = []
    for i in freqSortedLetters:
        placeData = occuranceDict[i]
        for j in range(1,len(placeData)):
            if placeData[j][2] in occupiedPositions:
                continue
            newDict[placeData[0]] = placeData[j][2]
            occupiedPositions.append(placeData[j][2])
            break
    return newDict

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
previousBest = mobileFitness(lowerInput, letterNum)
testBest = 100 #arbitrarily large
possibleSwaps = itertools.combinations(letterNum, 2)
possibleSwaps = [list(i) for i in possibleSwaps]
if __name__ == '__main__':
    randomGradient(5,'pickleTest')

    lettersAreHere = resultsTraverser('pickleTest')
    # strongestOccuringLetters = returnStrongestLetterPlacements(lettersAreHere)
    # print 'strongestOccuringLetters', strongestOccuringLetters
    # for i in range(29):
    #     theoreticalBestKeyboard = strongestKeyboard(lettersAreHere, i)
    #     print i, mobileFitness(lowerInput, theoreticalBestKeyboard)
    # print '\n', theoreticalBestKeyboard
    theoreticalBestKeyboard = strongestKeyboard(lettersAreHere, 28)
    print mobileFitness(lowerInput, theoreticalBestKeyboard), keyboardDisplay(theoreticalBestKeyboard)

    bestOfPickles = getMinKeyboard('pickleTest')
    print bestOfPickles[0], keyboardDisplay(bestOfPickles[1])
