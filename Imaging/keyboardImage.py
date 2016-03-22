from wand.image import Image
letters = [
'q','w','e','r','t','y','u','i','o','p',
'a','s','d','f','g','h','j','k','l',
'^','z','x','c','v','b','n','m',
' ']

numCoord = {1: [0, 3], 2: [1, 3], 3: [2, 3], 4: [3, 3], 5: [4, 3], 6: [5, 3], 7: [6, 3], 8: [7, 3], 9: [8, 3], 10: [9, 3], 11: [0.5, 2], 12: [1.5, 2], 13: [2.5, 2], 14: [3.5, 2], 15: [4.5, 2], 16: [5.5, 2], 17: [6.5, 2], 18: [7.5, 2], 19: [8.5, 2], 20: [0, 0], 21: [1.5, 1], 22: [2.5, 1], 23: [3.5, 1], 24: [4.5, 1], 25: [5.5, 1], 26: [6.5, 1], 27: [7.5, 1], 28: [5.5, 0]}
letterNum = {' ': 28, '^': 20, 'a': 11, 'c': 23, 'b': 25, 'e': 3, 'd': 13, 'g': 15, 'f': 14, 'i': 8, 'h': 16, 'k': 18, 'j': 17, 'm': 27, 'l': 19, 'o': 9, 'n': 26, 'q': 1, 'p': 10, 's': 12, 'r': 4, 'u': 7, 't': 5, 'w': 2, 'v': 24, 'y': 6, 'x': 22, 'z': 21}

def makeKeyboardImage(dict1):
	# for i in letters:
	#	 print ("convert -size 100x100 xc:transparent '{0}.png'".format(i))
	#	 print ("convert '{0}.png' -fill white -stroke black -strokewidth 3 -draw 'rectangle 3,3 96,96' {0}.png -gravity Center -fill black -stroke black -pointsize 70 -annotate 0 '{0}' {0}.png".format(i))
	w = 1000
	h = 400
	with Image(width=w, height=h, background=None) as board:
		for i in letters:
			if i == ' ':
				name = '_.png'
			else:
				name = i+'.png'
			with Image(filename=name) as key:
				board.composite(key, left=int(numCoord[letterNum[i]][0]*100), top=(h-int(numCoord[letterNum[i]][1]*100))-100)
		board.save(filename='KEYBOARD.png')

makeKeyboardImage(letterNum)

