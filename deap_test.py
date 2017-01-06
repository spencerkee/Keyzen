import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import math

def create_keyboard(input_chars):
    return random.sample(input_chars,len(input_chars))

def distance(p0, p1):#simple distance formula
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def indices_to_keyboard(input_indices):
    keyboard = []
    for index in input_indices:
        keyboard.append(CHARACTERS[index])
    return keyboard

def frequencyFitness(input_indices):
    keyboard = indices_to_keyboard(input_indices)
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

    return (fitness_score,)

#What creator.create does is that it creates a new class. Its name is the first argument of the function.
# Here on the first line we create a class named FitnessMax().base.Fitness tells you that this class is derived from the class base.Fitness().weight() is explained in the tutorial.

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# On the second line we create a class named Individual() derived from a list. We add the class creator.Fitness as one of its additionnal attribute.
creator.create("Individual", list, fitness=creator.FitnessMin)

CHARACTERS = 'qwertyuiopasdfghjkl^zxcvbnm '
NUM_POPULATION = 100

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(CHARACTERS)), len(CHARACTERS))
# container – The type to put in the data from func.
# generator – A function returning an iterable (list, tuple, ...), the content of this iterable will fill the container.
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)

toolbox.register("population", tools.initRepeat, list, 
                 toolbox.individual)
toolbox.register("evaluate", frequencyFitness)
#ordered crossover
toolbox.register("mate", tools.cxOrdered)
#mutation we will swap elements from two points of the individual.
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# ind1 = toolbox.individual()
# print (ind1)
# ind1.fitness.values = frequencyFitness(ind1)



pop = toolbox.population(n=NUM_POPULATION)
result, log = algorithms.eaSimple(pop, toolbox,
                             cxpb=0.8, mutpb=0.2,
                             ngen=10, verbose=False)
best_individual = tools.selBest(result, k=1)[0]
print (best_individual)