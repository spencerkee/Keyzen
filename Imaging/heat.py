from __future__ import division
import heatmap
import random
from collections import Counter

def mapping(keyboard):
	coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
	[0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
	[0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
	[5.5,0]]
	adjustedCoordinates = []
	for i in coordinates:
		y = (i[0]*100)
		x = (i[1]*100)
		adjustedCoordinates.append([y,x])
	pts = []
	# #will need to fetch this at the time
	# frequencyData = Counter({' ': 625, 'e': 315, 't': 274, 'o': 222, 'a': 198, 'h': 175, 'i': 168, 'n': 164, 's': 155, 'r': 139, 'd': 116, 'l': 111, 'w': 84, 'u': 71, '^': 58, 'f': 57, 'g': 53, 'c': 49, 'b': 46, 'y': 43, 'p': 40, 'm': 37, 'k': 29, 'v': 25, 'j': 3, 'q': 1, 'x': 1})

	# freqDict = {'v':0,'h':0,'t':0,'d':0,'z':0,'u':0,'^':0,'g':0,'c':0,'k':0,'o':0,' ':0,'a':0,'q':0,'r':0,'p':0,'e':0,'i':0,'l':0,'w':0,'n':0,'b':0,'x':0,'m':0,'s':0,'f':0,'y':0,'j':0}
	# for i in frequencyData:
	# 	freqDict[i] = int((frequencyData[i]/3259)*150)
	# print freqDict
	# ind = 0
	# modifier=20
	# for letter in keyboard:
	# 	for j in range(freqDict[letter]):
	# 		y = adjustedCoordinates[ind][0]
	# 		x = adjustedCoordinates[ind][1]-100
	# 		# y = random.randint(adjustedCoordinates[ind][0],adjustedCoordinates[ind][0]+modifier)
	# 		# x = random.randint(adjustedCoordinates[ind][1],adjustedCoordinates[ind][1]+modifier)
	# 		pts.append((y,x))
	# 	ind+=1
	for i in range(5):
		pts.append([100,100])
		# pts.append(adjustedCoordinates[0])
	print pts
	print "Processing %d points..." % len(pts)

	hm = heatmap.Heatmap()
	img = hm.heatmap(pts,size=(1000,400),dotsize=150)
	img.save("classic.png")

mapping('xahtusngzqweoir dpkjvfb^lmcy')
#if a key 