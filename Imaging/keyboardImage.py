from wand.image import Image
def makeKeyboardImage(thisDict):
	keyNumberToCoordinates = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}
	letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','^','z','x','c','v','b','n','m',' ']
	if isinstance(thisDict['q'], int):
		print (thisDict)
		newDict = {}
		for i in thisDict:
			newDict[i] = keyNumberToCoordinates[thisDict[i]]
		thisDict = newDict
	print (thisDict)
	w = 1000
	h = 400
	with Image(width=w, height=h, background=None) as board:
		for i in letters:
			if i == ' ':
				name = '_.png'
			else:
				name = i+'.png'
			with Image(filename=name) as key:
				board.composite(key, left=int(thisDict[i][0]*100), top=(h-int(thisDict[i][1]*100))-100)
		board.save(filename='KEYBOARD.png')
if __name__ == '__main__':
	minimum = {' ': 17, '^': 5, 'a': 13, 'c': 9, 'b': 15, 'e': 18, 'd': 26, 'g': 16, 'f': 21, 'i': 7, 'h': 4, 'k': 24, 'j': 25, 'm': 27, 'l': 22, 'o': 12, 'n': 3, 'q': 1, 'p': 19, 's': 23, 'r': 2, 'u': 11, 't': 8, 'w': 14, 'v': 10, 'y': 6, 'x': 28, 'z': 20}
	makeKeyboardImage(minimum)
 		# for i in letters:
	#	 print ("convert -size 100x100 xc:transparent '{0}.png'".format(i))
	#	 print ("convert '{0}.png' -fill white -stroke black -strokewidth 3 -draw 'rectangle 3,3 96,96' {0}.png -gravity Center -fill black -stroke black -pointsize 70 -annotate 0 '{0}' {0}.png".format(i))
