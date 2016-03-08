#!/usr/bin/env python2.7
from __future__ import division
import pickle
import collections

def most_common(lst):
    return max(set(lst), key=lst.count)
def invertDict(thisDict):
	newDict = {}
	for k in thisDict:
		newDict[thisDict[k]] = k
	return newDict

lists = []
infile = open('pickleTest', 'r')
while 1:
    try:
        lists.append(pickle.load(infile))
    except (EOFError):
        break
infile.close()
resultsNum = len(lists)
print "There are", resultsNum, "results"
#
letterOccurances = {}
letters = [
'q','w','e','r','t','y','u','i','o','p',
'a','s','d','f','g','h','j','k','l',
'^','z','x','c','v','b','n','m',
' ']

dupe = []
for i in letters:
    letterOccurances[i] = []
for j in lists:
    dupe.append(j[1])
    for key in j[1]:
        letterOccurances[key] = letterOccurances[key] + [j[1][key]]

dupe2 = [dict(t) for t in set([tuple(d.items()) for d in dupe])]
if len(dupe2) != resultsNum:
    print "DUPLICATES EXIST"
else:
    print "NO DUPLICATES"
fixedLO = {}
for k in letterOccurances:
    counter=collections.Counter(letterOccurances[k])
    fixedLO[k] = counter.most_common(4)

freqSortedLetters = [' ','e','t','a','o','l','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
qwer = {' ': 28, '^': 20, 'a': 11, 'c': 23, 'b': 25, 'e': 3, 'd': 13, 'g': 15, 'f': 14, 'i': 8, 'h': 16, 'k': 18, 'j': 17, 'm': 27, 'l': 19, 'o': 9, 'n': 26, 'q': 1, 'p': 10, 's': 12, 'r': 4, 'u': 7, 't': 5, 'w': 2, 'v': 24, 'y': 6, 'x': 22, 'z': 21}
qwer = invertDict(qwer)

for l in fixedLO:
    line = [l]
    for y in fixedLO[l]:
        line.append([qwer[y[0]], round((y[1]/resultsNum)*100,1), y[0]])
    fixedLO[l] = line

for p in freqSortedLetters:
    print fixedLO[p]

# th he in er an re nd at on nt ha es st en ed to it
#The most common first letter in a word in order of frequency
# T, O, A, W, B, C, D, S, F, M, R, H, I, Y, E, G, L, N, O, U, J, K
# More than half of all words end with
# E ,T, D, S
x = [2.84,20.4,7.9,10.9,17.5,9.3,9.3,8.0,7.5,9.0,7.6,9.3,7.8,7.9,8.8,7.1,8.4,7.6,11.1,9.0,8.5,9.9,12.3,16.4,42.2,15.1,37.6,10.4]
x.sort(reverse = True)
print x
