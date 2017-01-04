#!/usr/bin/python2.7
# -*- coding: utf-8 -*-1
from __future__ import division
import sys
import random
import numpy
import math
import time
import itertools
from collections import Counter
start_time = time.time()
import collections#need to correct


theInput = '''Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.
'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)
Down, down, down. Would the fall never come to an end! 'I wonder how many miles I've fallen by this time?' she said aloud. 'I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think' (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) 'yes, that's about the right distancebut then I wonder what Latitude or Longitude I've got to?' (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)'''



letterString = 'qwertyuiopasdfghjkl^zxcvbnm '

def distance(p0, p1):#simple distance formula
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def createNKeyboards(n):#generates n keyboards in the form of scrambled letterString
    returnList = []
    for i in range(n):
        returnList.append(''.join(random.sample(letterString,len(letterString))))
    return returnList

def processText(myInput):#removes symbols and changes capitals into lowercase letters prepended with ^. could be improved with exceptions
    firstMarker = 0
    stringList = []
    for i in range(0,len(myInput)):
        if myInput[i].isalpha() or myInput[i]==' ':
            if myInput[i].isupper():
                stringList.append(myInput[firstMarker:-(len(myInput)-i)])
                stringList.append('^{0}'.format(myInput[i].lower()))
                firstMarker = i+1
        else:
            stringList.append(myInput[firstMarker:-(len(myInput)-i)])
            firstMarker = i+1
    stringList.append(myInput[firstMarker:len(myInput)])
    return ''.join(stringList)

def stringFitnesses(inputText, keyboardStrings):#returns the list of fitnesses of a list of keyboards
    coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
    [0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
    [0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
    [5.5,0]]
    sameLetterCost = 0
    totalTransitions = len(inputText)
    distanceMatrix = numpy.zeros(shape=(len(letterString),len(letterString)))
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            distanceMatrix[i][j] = distance(coordinates[i],coordinates[j])
            distanceMatrix[j][i] = distanceMatrix[i][j]
    leftOnly = [0,1,2,3,4,10,11,12,13,19,20,21,22]#qwerasdfzxcv
    rightOnly = [5,6,7,8,9,15,16,17,18,24,25,26,27]#yuiophjklbn m

    returnList = []
    for individualKeyboard in keyboardStrings:
        letterNum = {}
        for i in range(len(letterString)):
            letterNum[individualKeyboard[i]] = i
        totalDistance = 0
        leftPosition = 13
        rightPosition = 16
        for letter in inputText:
            if letterNum[letter] == leftPosition or letterNum[letter] == rightPosition:
                totalDistance += sameLetterCost
            elif letterNum[letter] != leftPosition and letterNum[letter] != rightPosition:
                if letterNum[letter] in rightOnly:
                    totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
                    rightPosition = letterNum[letter]
                elif letterNum[letter] in leftOnly:
                    totalDistance += distanceMatrix[leftPosition, letterNum[letter]]
                    leftPosition = letterNum[letter]
                else:
                    if distanceMatrix[rightPosition, letterNum[letter]] <= distanceMatrix[leftPosition, letterNum[letter]]:
                        totalDistance += distanceMatrix[rightPosition, letterNum[letter]]
                        rightPosition = letterNum[letter]
                    else:
                        totalDistance += distanceMatrix[leftPosition, letterNum[letter]]
                        leftPosition = letterNum[letter]
        returnList.append((totalDistance/totalTransitions))
    return returnList

def mutateKeyboards(keyboardList, mutationPercent, swapNumber):
    returnList = []
    for i in keyboardList:
        if random.uniform(0,100) <= mutationPercent:
            lst = list(i)
            for l in range(swapNumber):
                indices = random.sample(range(0, len(i)), 2)
                j = indices[0]
                k = indices[1]
                lst[j], lst[k] = lst[k], lst[j]
            lst = (''.join(lst))
            returnList.append(lst)
        else:
            returnList.append(i)
    return returnList

def singlePointCrossover(parent1, parent2):
    crossoverPoint = random.randint(0,len(parent1)-1)
    newKeyboard = parent1[:crossoverPoint]
    addLetters = []
    for i in parent2:
        if i not in newKeyboard:
            addLetters.append(i)
    newKeyboard = newKeyboard + ''.join(addLetters)
    return newKeyboard

def simpleRouletteSelection(fitness_list):
    invertedList = [1/i for i in fitness_list]
    max = sum(invertedList)
    pick = random.uniform(0,max)
    currentValue = 0
    index = 0
    for i in invertedList:
        currentValue += i
        if currentValue > pick:
            break
        index+=1
    return fitness_list[index]

def simpleGeneticAlgorithm(keyboard_list, fitness_list, elite_num, death_percent):
    returnList = []
    while len(returnList) < len(keyboard_list)-elite_num:
        while True:
            parent1 = keyboard_list[fitness_list.index(simpleRouletteSelection(fitness_list))]
            parent2 = keyboard_list[fitness_list.index(simpleRouletteSelection(fitness_list))]
            child = singlePointCrossover(parent1,parent2)

            returnList.append(child)
            break

            # if stringFitnesses(theInput, [child])[0] < sum(stringFitnesses(theInput, [parent1,parent2]))/2:
            #   returnList.append(child)
            #   break
            # else:
            #   if random.uniform(0,100) >= death_percent:
            #       returnList.append(child)
            #       break

    # returnList = mutateKeyboards(returnList, 40, 3)
    returnList = mutateKeyboards(returnList, 2, 1)
    fitness_list.sort()
    for i in fitness_list[:elite_num]:
        returnList.append(keyboard_list[fitness_list.index(i)])
    return returnList

#this function must be broken, unique keyboard number is as low as 5 sometimes
def diversify(threshold, keyboard_list):#if a keyboard occurs more than (threshold) times, mutate all but 1 of them.
    count = Counter(keyboard_list)
    returnList = list(keyboard_list)
    for i in count.most_common():
        if i[1] >= threshold:
            returnList[:] = [x for x in returnList if x != i[0]]
            for j in range(i[1]-1):
                newKeyboard = mutateKeyboards([i[0]], 100, 1)[0]
                returnList.append(newKeyboard)
            returnList.append(i[0])
    return returnList

def gradientDescent():#should add a method to input something and see if any switch will make it better
    possSwaps = list(itertools.combinations(range(len(letterString)), 2))
    random.shuffle(possSwaps)
    keyboard = createNKeyboards(1)[0]
    # previousBest = stringFitnesses(theInput, [keyboard])[0]
    previousBest = frequencyFitness(keyboard)
    i = 0
    while i < len(letterString):
        lst = list(keyboard)
        indices = possSwaps[i]
        j = indices[0]
        k = indices[1]
        lst[j], lst[k] = lst[k], lst[j]
        lst = (''.join(lst))
        # if stringFitnesses(theInput, [lst])[0] < previousBest:
        #   previousBest = stringFitnesses(theInput, [lst])[0]
        if frequencyFitness(lst) < previousBest:
            previousBest = frequencyFitness(lst)
            keyboard = lst
            i = 0
            random.shuffle(possSwaps)
        else:
            lst = list(lst)
            lst[j], lst[k] = lst[k], lst[j]
            keyboard = (''.join(lst))
            i+=1
    return keyboard

def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: ' + sys.argv[0] + ' [numKeyboards] [numGenerations]')
    numKeyboards = int(sys.argv[1])
    if sys.argv[2] == 'inf':
        numGenerations = float('inf')
    else:
        numGenerations = int(sys.argv[2])

    newPopulation= createNKeyboards(numKeyboards)
    # newPopulation = [gradientDescent() for i in range(50)]
    i = 0
    bestScore = float('inf')
    bestKeyboard = ''

    printList = ["#", "Avg. Fitness", "Min. Fitness", "Min. Fitness Keyboard", "Best Score", "Best Keyboard", "Most Common (Keyboard, Occurences)"]
    # 15 spaces for scores, 30 for keyboard strings
    rowFormat ="{:<5}" + "{:<15}"*2 + "{:<30}" + "{:<15}" + "{:<30}"*2
    print rowFormat.format(*printList)
    while True:
        if i == numGenerations:
            print("--- %s seconds ---" % (time.time() - start_time))
            break
        # fitnesses = stringFitnesses(theInput, newPopulation)
        fitnesses = [frequencyFitness(keyboard) for keyboard in newPopulation]
        avg = sum(fitnesses)/len(fitnesses)
        minIndex = fitnesses.index(min(fitnesses))

        if min(fitnesses) < bestScore:
            bestScore = min(fitnesses)
            bestKeyboard = str(newPopulation[minIndex])
        count = Counter(newPopulation)
        if i % 100 == 0:
            print rowFormat.format(i, avg, min(fitnesses), newPopulation[minIndex], bestScore, bestKeyboard, count.most_common()[0]), len(count.most_common())

        newPopulation = simpleGeneticAlgorithm(newPopulation, fitnesses, 1, death_percent=80)
        newPopulation = diversify(4, newPopulation)

        i += 1
    print newPopulation[0]

def frequencyFitness(keyboard):
    fitness_score = 0
    # a b   c   d   e   f   g   h   i   j   k   l   m
    # 8.2   1.5 2.8 4.3 12.7    2.2 2.0 6.1 7.0 0.2 0.8 4.0 2.4
    # n o   p   q   r   s   t   u   v   w   x   y   z
    # 6.7   7.5 1.9 0.1 6.0 6.3 9.1 2.8 1.0 2.4 0.2 2.0 0.1
    coordinates = [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
    [0.5,2],[1.5,2],[2.5,2],[3.5,2],[4.5,2],[5.5,2],[6.5,2],[7.5,2],[8.5,2],
    [0,0],[1.5,1],[2.5,1],[3.5,1],[4.5,1],[5.5,1],[6.5,1],[7.5,1],
    [5.5,0]]
    # freq_dict = {'a':8.2,'b':1.5, 'c':2.8, 'd':4.3, 'e':12.7,'f':2.2,'g':2.0,'h':6.1,'i':7.0,'j':0.2,'k':0.8,'l':4.0,'m':2.4,
    # 'n':6.7,'o':7.5,'p':1.9,'q':0.1,'r':6.0,'s':6.3,'t':9.1,'u':2.8,'v':1.0,'w':2.4,'x':0.2,'y':2.0,'z':0.1, '^':2.8,' ':13.6}
    
    freq_dict = {'a':8.50357834949,'b':1.58827987693,'c':3.35831867318,'d':3.8332505962,'e':12.0854920097,'f':2.1435268052,'g':1.99366445597,
'h':4.72281799311,'i':7.28576061687,'j':0.221705546931,'k':0.778118038872,'l':4.07968142936,'m':2.64836003734,'n':7.27089968004,
'o':7.41507990637,'p':2.14681185439,'q':0.101035966795,'r':6.57070724088,'s':6.88783871261,'t':8.94593736877,'u':2.56241658647,
'v':1.04965603373,'w':1.72204517838,'x':0.201144083561,'y':1.77340052726,'z':0.110472431636, ' ':22.2596873, '^':5.41006961}

    # x = 0
    # for i in freq_dict:
    #   x += freq_dict[i]
    # print x

    for i in keyboard:
        left_distance = distance(coordinates[12],coordinates[keyboard.index(i)])
        right_distance = distance(coordinates[16],coordinates[keyboard.index(i)])
        fitness_score += min(left_distance,right_distance)*freq_dict[i]

    bigrams = {'th': 1.52,'en': 0.55,'ng': 0.18,'he':1.28,'ed':0.53,'of':0.16,'in':0.94,'to':0.52,'al':0.09,'er':0.94,'it': 0.50,'de':0.09,
     'an':0.82,'ou':0.50,'se': 0.08,'re': 0.68,'ea': 0.47,'le': 0.08,'nd': 0.63,'hi': 0.46,'sa': 0.06,'at': 0.59,'is': 0.46,'si': 0.05,
     'on': 0.57,'or': 0.43,'ar': 0.04,'nt': 0.56,'ti': 0.34,'ve': 0.04,'ha': 0.56,'as': 0.33,'ra': 0.04,'es': 0.56,'te': 0.27,'ld': 0.02,'st': 0.55,'et': 0.19,'ur': 0.02}
    leftOnly = [0,1,2,3,4,10,11,12,13,19,20,21,22]#qwerasdfzxcv
    rightOnly = [5,6,7,8,9,15,16,17,18,24,25,26,27]#yuiophjklbn m
    for bigram in bigrams:
        left_position = 12
        right_position = 16
        for i in bigram:
            if keyboard.index(i) in leftOnly:
                fitness_score += distance(coordinates[12],coordinates[keyboard.index(i)])
                left_position = keyboard.index(i)
            elif keyboard.index(i) in rightOnly:
                right_distance = distance(coordinates[16],coordinates[keyboard.index(i)])
                right_position = keyboard.index(i)
            else:
                left_distance = distance(coordinates[left_position],coordinates[keyboard.index(i)])
                right_distance = distance(coordinates[right_position],coordinates[keyboard.index(i)])
                if left_distance < right_distance:
                    left_position = keyboard.index(i)
                    fitness_score += left_distance
                else:
                    right_position = keyboard.index(i)
                    fitness_score += right_distance

    return fitness_score

if __name__ == '__main__':
    theInput = processText(theInput)


    # min2 = 'qforbvlwkx^teuya hjzingpdscm'
    # # print frequencyFitness(min2)
    # print frequencyFitness('zpl^wyshgqvo rmieakxctdbfnuj')
    print frequencyFitness('qyanuc^lgjbt rkheivfspwmodzx')
    print frequencyFitness('qwertyuiopasdfghjkl^zxcvbnm ')

    # print ''
    # # print stringFitnesses(theInput, ['qysrufhdwjvnaebo igxmtpzc^lk'])[0]
    # print stringFitnesses(theInput, ['zpl^wyshgqvo rmieakxctdbfnuj'])[0]
    # print stringFitnesses(theInput, ['qwertyuiopasdfghjkl^zxcvbnm '])[0]


    # random_keyboards = createNKeyboards(50)
    # print random_keyboards
    # x = [frequencyFitness(keyboard) for keyboard in random_keyboards]
    # print x
    # print ''
    # seq = sorted(x)
    # index = [seq.index(v) for v in x]
    # print index

    # x = [stringFitnesses(theInput, [keyboard])[0] for keyboard in random_keyboards]
    # print x
    # print ''
    # seq = sorted(x)
    # index2 = [seq.index(v) for v in x]
    # print index2

    # total_difference = 0
    # for i in range(50):
    #   total_difference += abs(index[i]-index2[i])
    # print total_difference/50






    # letters = collections.Counter(theInput)
    # for i in letters:
    #   letters[i] = letters[i]/32.59
    # print letters
    # print len(theInput)


    main()
# 

    # for i in range(100):
    #   x = gradientDescent()
    #   if frequencyFitness(x) < 115:
    #       print x, frequencyFitness(x)

    
    # print stringFitnesses(theInput, [min2])[0]





# x = [
# 'A', 280937 ,5263779, 
# 'B', 169474 ,866156, 
# 'C', 229363 ,1960412, 
# 'D', 129632 ,2369820, 
# 'E', 138443 ,7741842, 
# 'F', 100751, 1296925, 
# 'G', 93212 ,1206747,
# 'H', 123632 ,2955858 ,
# 'I', 223312 ,4527332,
# 'J', 78706 ,65856 ,
# 'K', 46580 ,460788 ,
# 'L', 106984 ,2553152,
# 'M', 259474 ,1467376,
# 'N', 205409 ,4535545 ,
# 'O', 105700 ,4729266 ,
# 'P', 144239 ,1255579 ,
# 'Q', 11659 ,54221,
# 'R', 146448 ,4137949 ,
# 'S', 304971 ,4186210,
# 'T', 325462 ,5507692 ,
# 'U', 57488 ,1613323,
# 'V', 31053 ,653370,
# 'W', 107195 ,1015656 ,
# 'X', 7578 ,123577,
# 'Y', 94297 ,1062040 ,
# 'Z', 5610, 66423]
# first = 1
# second = 2
# lower_total = 0
# upper_total = 0
# while second <= len(x):
#   # print 'first', x[first], 'second', x[second]
#   upper_total += x[first]
#   lower_total += x[second]
#   # print "'" + str(x[first].lower()) + "'" + ':' + str(x[second]/652045.03) + ','
#   first += 3
#   second += 3

# print upper_total
# print lower_total

# # total = 65204503/3527609