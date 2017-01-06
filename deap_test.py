import random

from deap import base
from deap import creator
from deap import tools

#What creator.create does is that it creates a new class. Its name is the first argument of the function.
# Here on the first line we create a class named FitnessMax().base.Fitness tells you that this class is derived from the class base.Fitness().weight() is explained in the tutorial.

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

characters = 'qwertyuiopasdfghjkl^zxcvbnm '

#toolbox = base.Toolbox() instanciates the object toolbox from the class base.Toolbox(). This object contains the method « register » which is widely used hereafter.
toolbox = base.Toolbox()
#toolbox.register(« attr_float », random.random) adds a method to the toolbox object. This method is referenced under the name « attr_float » and is actually copied from the function random.random. So calling the attr_float method is equivalent to calling the random.random function. To do so, you only have to do what you would do with any other method :
toolbox.register("indices", random.sample, characters, len(characters))
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)

print (toolbox.individual())