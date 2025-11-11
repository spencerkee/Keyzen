#!/usr/bin/env python2.7
from __future__ import division
from wand.image import Image
import math
from random import shuffle
from random import uniform
from random import choice

# import heatmap
from collections import Counter
import random
from pathlib import Path
import os


def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)


def makeKeyboardImage(thisDict, filename):
    keyNumberToCoordinates = {
        1: [0, 3],
        2: [1, 3],
        3: [2, 3],
        4: [3, 3],
        5: [4, 3],
        6: [5, 3],
        7: [6, 3],
        8: [7, 3],
        9: [8, 3],
        10: [9, 3],
        11: [0.5, 2],
        12: [1.5, 2],
        13: [2.5, 2],
        14: [3.5, 2],
        15: [4.5, 2],
        16: [5.5, 2],
        17: [6.5, 2],
        18: [7.5, 2],
        19: [8.5, 2],
        20: [0, 0],
        21: [1.5, 1],
        22: [2.5, 1],
        23: [3.5, 1],
        24: [4.5, 1],
        25: [5.5, 1],
        26: [6.5, 1],
        27: [7.5, 1],
        28: [5.5, 0],
    }
    letters = [
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "a",
        "s",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "^",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
        " ",
    ]
    if isinstance(thisDict["q"], int):
        newDict = {}
        for i in thisDict:
            newDict[i] = keyNumberToCoordinates[thisDict[i]]
        thisDict = newDict
    w = 1000
    h = 400
    with Image(width=w, height=h, background=None) as board:
        for i in letters:
            if i == " ":
                name = "_.png"
            else:
                name = i + ".png"
            with Image(filename=name) as key:
                board.composite(
                    key,
                    left=int(thisDict[i][0] * 100),
                    top=(h - int(thisDict[i][1] * 100)) - 100,
                )
        board.save(filename=filename + ".png")


def makeStringImage(inputString, filename):  # filename must include extension
    imaging_dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    coordinates = [
        [0, 3],
        [1, 3],
        [2, 3],
        [3, 3],
        [4, 3],
        [5, 3],
        [6, 3],
        [7, 3],
        [8, 3],
        [9, 3],
        [0.5, 2],
        [1.5, 2],
        [2.5, 2],
        [3.5, 2],
        [4.5, 2],
        [5.5, 2],
        [6.5, 2],
        [7.5, 2],
        [8.5, 2],
        [0, 0],
        [1.5, 1],
        [2.5, 1],
        [3.5, 1],
        [4.5, 1],
        [5.5, 1],
        [6.5, 1],
        [7.5, 1],
        [5.5, 0],
    ]
    w = 1000
    h = 400
    with Image(width=w, height=h, background=None) as board:
        for i in range(len(inputString)):
            if inputString[i] == " ":
                name = "_.png"
            else:
                name = inputString[i] + ".png"

            filepath = imaging_dir_path / name

            with Image(filename=filepath) as letter:
                board.composite(
                    letter,
                    left=int(coordinates[i][0] * 100),
                    top=(h - int(coordinates[i][1] * 100)) - 100,
                )
        board.save(filename=filename)


def mapping(keyboard):
    coordinates = [
        [0, 3],
        [1, 3],
        [2, 3],
        [3, 3],
        [4, 3],
        [5, 3],
        [6, 3],
        [7, 3],
        [8, 3],
        [9, 3],
        [0.5, 2],
        [1.5, 2],
        [2.5, 2],
        [3.5, 2],
        [4.5, 2],
        [5.5, 2],
        [6.5, 2],
        [7.5, 2],
        [8.5, 2],
        [0, 0],
        [1.5, 1],
        [2.5, 1],
        [3.5, 1],
        [4.5, 1],
        [5.5, 1],
        [6.5, 1],
        [7.5, 1],
        [5.5, 0],
    ]
    adjustedCoordinates = []
    for i in coordinates:
        x = (i[1] * 100) + 50  # moves up
        y = (i[0] * 100) + 50
        adjustedCoordinates.append([y, x])
    pts = []

    # # #will need to fetch this at the time
    frequencyData = Counter(
        {
            " ": 625,
            "e": 315,
            "t": 274,
            "o": 222,
            "a": 198,
            "h": 175,
            "i": 168,
            "n": 164,
            "s": 155,
            "r": 139,
            "d": 116,
            "l": 111,
            "w": 84,
            "u": 71,
            "^": 58,
            "f": 57,
            "g": 53,
            "c": 49,
            "b": 46,
            "y": 43,
            "p": 40,
            "m": 37,
            "k": 29,
            "v": 25,
            "j": 3,
            "q": 1,
            "x": 1,
        }
    )

    freqDict = {
        "v": 0,
        "h": 0,
        "t": 0,
        "d": 0,
        "z": 0,
        "u": 0,
        "^": 0,
        "g": 0,
        "c": 0,
        "k": 0,
        "o": 0,
        " ": 0,
        "a": 0,
        "q": 0,
        "r": 0,
        "p": 0,
        "e": 0,
        "i": 0,
        "l": 0,
        "w": 0,
        "n": 0,
        "b": 0,
        "x": 0,
        "m": 0,
        "s": 0,
        "f": 0,
        "y": 0,
        "j": 0,
    }
    for i in frequencyData:
        freqDict[i] = int((frequencyData[i] / 3259) * 150)
    print(freqDict)
    ind = 0
    modifier = 0
    for letter in keyboard:
        for j in range(freqDict[letter]):
            # y = adjustedCoordinates[ind][0]
            # x = adjustedCoordinates[ind][1]
            y = random.randint(
                adjustedCoordinates[ind][0] - modifier,
                adjustedCoordinates[ind][0] + modifier,
            )
            x = random.randint(
                adjustedCoordinates[ind][1] - modifier,
                adjustedCoordinates[ind][1] + modifier,
            )
            pts.append((y, x))
        ind += 1
    # for i in range(30):
    # pts.append([500,200]	)
    # coord = [random.uniform(0,1000),random.uniform(0,400)]
    # coord = [610.5626187013722, 4.879347488184216]
    # pts.append(coord)
    # pts.append(adjustedCoordinates[0])
    pts.append([0, 0])
    pts.append([0, 400])
    pts.append([1000, 0])
    pts.append([1000, 400])
    print(pts)
    print("Processing %d points..." % len(pts))

    hm = heatmap.Heatmap()
    img = hm.heatmap(pts, size=(1000, 400), dotsize=150)
    img.save("classic.png")


# mapping('qforbvlwkx^teuya hjzingpdscm')
# mapping('qwertyuiopasdfghjkl^zxcvbnm ')
# makeStringImage('qyanuc^lgjbt rkheivzfspwmodx', 'FREQMIN.png')#115.12
# makeStringImage('qwertyuiopasdfghjkl^zxcvbnm ', 'STRINGTEST.png')
