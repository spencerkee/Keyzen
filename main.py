import math
import random
from pprint import pprint
import ipdb
from deap import creator, base, tools, algorithms
import numpy

CHARACTERS = "qwertyuiopasdfghjkl^zxcvbnm "


def alphabetical_fitness(individual):
    sorted_characters = sorted(CHARACTERS)
    individual_as_characters = [CHARACTERS[i] for i in individual]
    fitness_score = 0
    for i, char in enumerate(individual_as_characters):
        if char == sorted_characters[i]:
            fitness_score += 1
    return (fitness_score,)


def create_toolbox(indpb, tournsize):
    # We have a single fitness function that we want to minimize/maximize
    # creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # creator.create("Individual", list, fitness=creator.FitnessMax)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    # Create an individual consisting of randomized characters from CHARACTERS.
    toolbox.register("indices", random.sample, range(len(CHARACTERS)), len(CHARACTERS))
    toolbox.register(
        "individual", tools.initIterate, creator.Individual, toolbox.indices
    )
    # Create a population of individuals.
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", alphabetical_fitness)
    # We use ordered crossover
    toolbox.register("mate", tools.cxOrdered)
    # For mutation we will swap elements from two points on the individual.
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=indpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    return toolbox


def main():
    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    # NGEN is the number of generations before quitting
    CXPB, MUTPB, NGEN = 0.5, 0.2, 90
    # Independent probability for each attribute to be exchanged to another position.
    indpb = 0.05
    # The number of individuals participating in each tournament.
    tournsize = 30

    toolbox = create_toolbox(indpb, tournsize)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=CXPB,
        mutpb=MUTPB,
        ngen=NGEN,
        stats=stats,
        halloffame=hof,
        verbose=True,
    )

    best_individual = hof[0]
    best_individual_as_characters = "".join([CHARACTERS[i] for i in best_individual])
    print(
        f"Best individual: {best_individual_as_characters} with fitness: {best_individual.fitness.values}"
    )


# uv run main.py
if __name__ == "__main__":
    main()
