#!/usr/bin/env python2.7
from __future__ import division
import pickle
import collections
import copy
from randomGradient import keyboardDisplay, invertDict

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

def getMinKeyboard(pickledResults):
    return min(pickledResults)[0][1]

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
    # print lettersAreHere['a']
    for l in lettersAreHere:
        line = [l]
        for y in lettersAreHere[l]:
            line.append([qwer[y[0]], round((y[1]/resultsNum)*100,1), y[0]])
        lettersAreHere[l] = line
    # print lettersAreHere['a']
    return lettersAreHere

def returnStrongestLetterPlacements(percentOccuranceDict):#returns list of keys that strongly tend to one position
    freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
    strongestOccuringLetters = []
    for p in freqSortedLetters:
        strongestOccuringLetters.append([lettersAreHere[p][1][1], lettersAreHere[p][0]])
    strongestOccuringLetters.sort(reverse = True)
    return strongestOccuringLetters

def strongestKeyboard(occuranceDict):#greedy algorithm that itereates over frequencySortedLetters and places letters in their strongest position that isn't already filled
    freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
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

lettersAreHere = resultsTraverser('pickleTest')
strongestOccuringLetters = returnStrongestLetterPlacements(lettersAreHere)
print 'strong', strongestOccuringLetters
theoreticalBestKeyboard = strongestKeyboard(lettersAreHere)
print keyboardDisplay(theoreticalBestKeyboard)

# # th he in er an re nd at on nt ha es st en ed to it
# #The most common first letter in a word in order of frequency
# # T, O, A, W, B, C, D, S, F, M, R, H, I, Y, E, G, L, N, O, U, J, K
# # More than half of all words end with
# # E ,T, D, S
