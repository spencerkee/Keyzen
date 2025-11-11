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


def create_toolbox():
    # We have a single fitness function that we want to maximize
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", str, fitness=creator.FitnessMax)

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
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


# def old_main():
#     toolbox = create_toolbox()
#     # CXPB  is the probability with which two individuals are crossed
#     # MUTPB is the probability for mutating an individual
#     CXPB, MUTPB = 0.5, 0.2

#     # Variable keeping track of the number of generations
#     generation_num = 0
#     # Begin the evolution
#     while generation_num < 100:
#         # A new generation
#         generation_num += 1
#         print("-- Generation %i --" % generation_num)

#         best_individual = tools.selBest(population, k=1)[0]
#         best_individual_as_characters = "".join(
#             [CHARACTERS[i] for i in best_individual]
#         )
#         print(
#             f"Best individual: {"".join(best_individual_as_characters)} with fitness: {best_individual.fitness.values}"
#         )

#         offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
#         fits = toolbox.map(toolbox.evaluate, offspring)
#         for fit, ind in zip(fits, offspring):
#             ind.fitness.values = fit
#         population = toolbox.select(offspring, k=len(population))
#     print("".join(sorted(CHARACTERS)))


def main():
    toolbox = create_toolbox()

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    # NGEN is the number of generations before quitting
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40

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


if __name__ == "__main__":
    main()
