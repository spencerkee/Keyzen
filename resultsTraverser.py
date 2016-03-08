#!/usr/bin/env python2.7
from __future__ import division
import pickle
import collections
import copy
from randomGradient import keyboardDisplay
from randomGradient import invertDict
from randomGradient import mobileFitness

def most_common(lst):
    return max(set(lst), key=lst.count)

lists = []
infile = open('pickleTest', 'r')
index = 0
while 1:
    try:
        lists.append([pickle.load(infile),index])
    except (EOFError):
        break
    index += 1
infile.close()

print min(lists)

k = {' ': 17, '^': 5, 'a': 13, 'c': 9, 'b': 15, 'e': 18, 'd': 26, 'g': 16, 'f': 21, 'i': 7, 'h': 4, 'k': 24, 'j': 25, 'm': 27, 'l': 22, 'o': 12, 'n': 3, 'q': 1, 'p': 19, 's': 23, 'r': 2, 'u': 11, 't': 8, 'w': 14, 'v': 10, 'y': 6, 'x': 28, 'z': 20}
print keyboardDisplay(k)
# resultsNum = len(lists)
# print "There are", resultsNum, "results"
# #
# letterOccurances = {}
# letters = [
# 'q','w','e','r','t','y','u','i','o','p',
# 'a','s','d','f','g','h','j','k','l',
# '^','z','x','c','v','b','n','m',
# ' ']
#
# dupe = []
# for i in letters:
#     letterOccurances[i] = []
# for j in lists:
#     dupe.append(j[1])
#     for key in j[1]:
#         letterOccurances[key] = letterOccurances[key] + [j[1][key]]
#
# dupe2 = [dict(t) for t in set([tuple(d.items()) for d in dupe])]
# if len(dupe2) != resultsNum:
#     print "DUPLICATES EXIST"
# else:
#     print "NO DUPLICATES"
# fixedLO = {}
# for k in letterOccurances:
#     counter=collections.Counter(letterOccurances[k])
#     fixedLO[k] = counter.most_common(28)
#
# freqSortedLetters = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','^']
# qwer = {' ': 28, '^': 20, 'a': 11, 'c': 23, 'b': 25, 'e': 3, 'd': 13, 'g': 15, 'f': 14, 'i': 8, 'h': 16, 'k': 18, 'j': 17, 'm': 27, 'l': 19, 'o': 9, 'n': 26, 'q': 1, 'p': 10, 's': 12, 'r': 4, 'u': 7, 't': 5, 'w': 2, 'v': 24, 'y': 6, 'x': 22, 'z': 21}
# qwer = invertDict(qwer)
#
# for l in fixedLO:
#     line = [l]
#     for y in fixedLO[l]:
#         line.append([qwer[y[0]], round((y[1]/resultsNum)*100,1), y[0]])
#     fixedLO[l] = line
#
# x = []
# for p in freqSortedLetters:
#     # print fixedLO[p][0],fixedLO[p][1],fixedLO[p][2],fixedLO[p][3],fixedLO[p][4],
#     print fixedLO[p][0], fixedLO[p][1], fixedLO[p][2], fixedLO[p][3], fixedLO[p][4]
#     x.append([fixedLO[p][1][1], fixedLO[p][0]])
#
# newDict = {}
# occupiedPositions = []
# for i in freqSortedLetters:
#     placeData = fixedLO[i]
#     for j in range(1,len(placeData)):
#         if j == len(placeData):
#             print 'thing', i
#         if placeData[j][2] in occupiedPositions:
#             continue
#         newDict[placeData[0]] = placeData[j][2]
#         occupiedPositions.append(placeData[j][2])
#         break
#
# print ''
# print newDict
# print keyboardDisplay(newDict)
# print mobileFitness(newDict)
#
# # th he in er an re nd at on nt ha es st en ed to it
# #The most common first letter in a word in order of frequency
# # T, O, A, W, B, C, D, S, F, M, R, H, I, Y, E, G, L, N, O, U, J, K
# # More than half of all words end with
# # E ,T, D, S
# x.sort(reverse = True)
# print x
