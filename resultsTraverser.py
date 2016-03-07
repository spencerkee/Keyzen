#!/usr/bin/env python2.7

import pickle
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

print "There are", len(lists), "results"
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
print "dupe", len(dupe2)
fixedLO = {}
for k in letterOccurances:
    fixedLO[k] = most_common(letterOccurances[k])

freqSortedLetters = [' ','e','t','a','o','l','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
qwer = {' ': 28, '^': 20, 'a': 11, 'c': 23, 'b': 25, 'e': 3, 'd': 13, 'g': 15, 'f': 14, 'i': 8, 'h': 16, 'k': 18, 'j': 17, 'm': 27, 'l': 19, 'o': 9, 'n': 26, 'q': 1, 'p': 10, 's': 12, 'r': 4, 'u': 7, 't': 5, 'w': 2, 'v': 24, 'y': 6, 'x': 22, 'z': 21}
qwer = invertDict(qwer)
for l in freqSortedLetters:
    print l, "goes to", qwer[fixedLO[l]]
