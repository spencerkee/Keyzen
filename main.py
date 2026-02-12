import math
import random
from pprint import pprint
import ipdb
from deap import creator, base, tools, algorithms
import numpy
from Imaging.keyboardImage import makeStringImage
from fitness.latency_map import get_fitness
from second_simpy_test import get_distance_for_chromosome, preprocess_input_text, predict_distance_for_chromosome
from simpy_keyboard import TEXT_INPUT, TEXT_INPUT_2
import time
import sys
import select
import datetime
from pathlib import Path
from collections import Counter

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

    # toolbox.register(
    #     "evaluate",
    #     predict_distance_for_chromosome
    # )


    # We use ordered crossover
    toolbox.register("mate", tools.cxOrdered)
    # For mutation we will swap elements from two points on the individual.
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=indpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    # toolbox.register("select", tools.selRoulette)

    return toolbox

def to_char(lst):
    return "".join([CHARACTERS[i] for i in best_individual])

def to_list(chars):
    return [CHARACTERS.index(i) for i in chars]


def make_kbd_layout(chromosome):
    cs = list(chromosome)
    cs[cs.index(' ')] = 'space'
    cs[cs.index('^')] = 'shift'
    kbd_layout = \
f"""[layout]
{" ".join(cs[:10])}
{" ".join(cs[10:19])}
{" ".join(cs[19:27])} bck
, . {" ".join(cs[27:])} return"""
    return kbd_layout

def main():
    # POP_SIZE is the number of individuals in each generation
    POP_SIZE = 300
    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    # NGEN is the number of generations before quitting
    CXPB, MUTPB, NGEN = 0.5, 0.5, 3
    # Independent probability for each attribute to be exchanged to another position.
    indpb = 0.05
    # The number of individuals participating in each tournament.
    tournsize = int(POP_SIZE * 0.05)

    preprocessed_input_text = preprocess_input_text(TEXT_INPUT_2)
    toolbox = create_toolbox(indpb, tournsize, preprocessed_input_text)

    pop = toolbox.population(n=POP_SIZE)

    # Try hardcoding some good individuals to see if that jumpstarts things
    pop[-1] = creator.Individual([CHARACTERS.index(i) for i in "xkbwugfsyzdath jrocp^evinmlq"])
    pop[-2] = creator.Individual([CHARACTERS.index(i) for i in "pdawjkbrmzuohytlescxgfv ^niq"])
    pop[-3] = creator.Individual([CHARACTERS.index(i) for i in "pdawzxbrmjuoh^eltscqfyv gnik"])


    hof = tools.HallOfFame(1)

    # Stats that depend on ind.fitness.values instead of just ind
    # stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean)
    # stats.register("std", numpy.std)
    # # stats.register("max", numpy.max)
    # stats.register("min", numpy.min)
    # # TODO There's got to be a better way of writing this lambda.
    # # Feels weird that pop isn't used.
    # stats.register("best", lambda _: "".join([CHARACTERS[i] for i in hof[0]]))
    # # stats.register("minval", lambda pop: print(pop[0]))
    # # stats.register("uniq", lambda pop: len(Counter([tuple(i) for i in pop])))

    stats = tools.Statistics(lambda ind: ind)
    stats.register("avg", lambda pop: round(numpy.mean([i.fitness.values for i in pop]), 2))
    stats.register("std", lambda pop: round(numpy.std([i.fitness.values for i in pop]), 2))
    # stats.register("max", numpy.max)
    stats.register("min", lambda pop: round(numpy.min([i.fitness.values for i in pop]), 2))
    # TODO There's got to be a better way of writing this lambda.
    # Feels weird that pop isn't used.
    # stats.register("minval", lambda pop: print(pop[0]))
    stats.register("bestval", lambda _: hof[0].fitness.values[0])
    stats.register("best", lambda _: "".join([CHARACTERS[i] for i in hof[0]]))
    stats.register("uniq", lambda pop: len(Counter([tuple(i) for i in pop])))

    total_gen = 0
    total_start = time.time()
    while True:
        start_time = time.time()
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
        duration = time.time() - start_time
        print(
            f"{NGEN} generations of {POP_SIZE} individuals completed in {duration:.2f} seconds"
        )
        total_gen += NGEN
        total_time = (time.time() - total_start)
        print(f"total_gen={total_gen} total_time={total_time:.2f}")

        # print(f"Generations per second {NGEN / duration:.2f}")

        best_individual = hof[0]
        best_individual_as_characters = "".join([CHARACTERS[i] for i in best_individual])
        best_individual_fitness = int(best_individual.fitness.values[0])
        print(
            f"Best individual: {best_individual_as_characters} with fitness: {best_individual_fitness}"
        )
        kbd_layout = make_kbd_layout(best_individual_as_characters)
        print(kbd_layout)

        datetime_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        filename = f"fit={best_individual_fitness} '{best_individual_as_characters}' date={datetime_str}.png"
        results_filepath = Path("Results") / filename
        makeStringImage(best_individual_as_characters, results_filepath)
        print("Breakpoint?")
        i, o, e = select.select( [sys.stdin], [], [], 10 )
        if (i):
          print("You said", sys.stdin.readline().strip())
          ipdb.set_trace()
          pass


# sudo apt update
# sudo apt-get install libmagickwand-dev
# uv run main.py
if __name__ == "__main__":
    main()
