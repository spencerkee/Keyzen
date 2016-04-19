from __future__ import division
import heatmap
import random
from collections import Counter

coordinates = [[0, 300],[100, 300],[200, 300],[300, 300],[400, 300],[500, 300],[600, 300],
[700, 300],[800, 300],[900, 300],[50.0, 200],[150.0, 200],[250.0, 200],[350.0, 200],
[450.0, 200],[550.0, 200],[650.0, 200],[750.0, 200],[850.0, 200],[0, 0],[150.0, 100],
[250.0, 100],[350.0, 100],[450.0, 100],[550.0, 100],[650.0, 100],[750.0, 100],[550.0, 0]]
# for i in coordinates:
# 	print str([i[0]*100,i[1]*100]) + ','
if __name__ == "__main__":	
	frequencyData = Counter({' ': 625, 'e': 315, 't': 274, 'o': 222, 'a': 198, 'h': 175, 'i': 168, 'n': 164, 's': 155, 'r': 139, 'd': 116, 'l': 111, 'w': 84, 'u': 71, '^': 58, 'f': 57, 'g': 53, 'c': 49, 'b': 46, 'y': 43, 'p': 40, 'm': 37, 'k': 29, 'v': 25, 'j': 3, 'q': 1, 'x': 1})
	pts = []
	freqDict = {}
	for i in frequencyData:
		print (frequencyData[i]/3259)*100
		freqDict[i] = int((frequencyData[i]/3259)*150)
	print freqDict
	ind = 0
	modifier=25
	for x in freqDict:
		for i in range(freqDict[x]):
			nearPoint = (random.randint(coordinates[ind][0],coordinates[ind][0]+modifier), random.randint(coordinates[ind][1],coordinates[ind][1]+modifier))
			pts.append(nearPoint)
		ind+=1
	print pts
	print "Processing %d points..." % len(pts)

	hm = heatmap.Heatmap()
	img = hm.heatmap(pts,size=(1000,400),dotsize=200)
	img.save("classic.png")