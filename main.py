import math
import random
from pprint import pprint
import ipdb
from deap import creator, base, tools, algorithms
import numpy
from Imaging.keyboardImage import makeStringImage
from fitness.latency_map import get_fitness
from second_simpy_test import get_distance_for_chromosome, preprocess_input_text
from simpy_keyboard import TEXT_INPUT

CHARACTERS = "qwertyuiopasdfghjkl^zxcvbnm "


def alphabetical_fitness(individual):
    sorted_characters = sorted(CHARACTERS)
    individual_as_characters = [CHARACTERS[i] for i in individual]
    fitness_score = 0
    for i, char in enumerate(individual_as_characters):
        if char == sorted_characters[i]:
            fitness_score += 1
    return (fitness_score,)


def create_toolbox(indpb, tournsize, preprocessed_input_text):
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

    # toolbox.register("evaluate", get_fitness)
    # toolbox.register("evaluate", alphabetical_fitness)
    # TODO If I don't set a keyword argument then then preprocessed_input text is set as the
    # chromosome argument. I should try to learn why that is.
    toolbox.register(
        "evaluate",
        get_distance_for_chromosome,
        preprocessed_input_text=preprocessed_input_text,
    )

    # We use ordered crossover
    toolbox.register("mate", tools.cxOrdered)
    # For mutation we will swap elements from two points on the individual.
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=indpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    return toolbox


def main():
    # POP_SIZE is the number of individuals in each generation
    POP_SIZE = 300
    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    # NGEN is the number of generations before quitting
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100
    # Independent probability for each attribute to be exchanged to another position.
    indpb = 0.05
    # The number of individuals participating in each tournament.
    tournsize = 30

    preprocessed_input_text = preprocess_input_text(TEXT_INPUT)
    toolbox = create_toolbox(indpb, tournsize, preprocessed_input_text)

    pop = toolbox.population(n=POP_SIZE)
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
    makeStringImage(best_individual_as_characters, "keyboard.png")


# sudo apt update
# sudo apt-get install libmagickwand-dev
# uv run main.py
if __name__ == "__main__":
    main()
