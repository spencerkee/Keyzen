from wand.image import Image

convert -size 100x100 xc:transparent 'q.png'
convert 'q.png' -size 100x100 -background transparent -fill white - stroke black -draw 'circle 50,50 98,49' -gravity Cenger -fill black -stroke black -pointsize 70 -annotate 0 'q' q.png

with Image(width=1000, height = 1000, background=None) as board:
	with Image(filename='q.png' as tile:
		board.composite(tile, left=500, top=500)