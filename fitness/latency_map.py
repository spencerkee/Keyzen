import math
import json
# original letter mapping
LETTER_COORDS = {
    "q": (0, 3),
    "w": (1, 3),
    "e": (2, 3),
    "r": (3, 3),
    "t": (4, 3),
    "y": (5, 3),
    "u": (6, 3),
    "i": (7, 3),
    "o": (8, 3),
    "p": (9, 3),
    "a": (0.5, 2),
    "s": (1.5, 2),
    "d": (2.5, 2),
    "f": (3.5, 2),
    "g": (4.5, 2),
    "h": (5.5, 2),
    "j": (6.5, 2),
    "k": (7.5, 2),
    "l": (8.5, 2),
    "^": (0, 1),
    "z": (1.5, 1),
    "x": (2.5, 1),
    "c": (3.5, 1),
    "v": (4.5, 1),
    "b": (5.5, 1),
    "n": (6.6, 1),
    "m": (7.5, 1),
    " ": (5.5, 0),
}

LETTER_TO_INDEX = {letter: index for index, letter in enumerate(LETTER_COORDS.keys())}
LEFT_LETTERS =set(["q", "w", "e", 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b', "^"]) 
LEFT_LETTER_INDEXES = set([LETTER_TO_INDEX[letter] for letter in LEFT_LETTERS])
RIGHT_LETTERS =set(["y", "u", "i", 'o', 'p', 'h', 'j', 'k', 'l', 'n', 'm', " "])
RIGHT_LETTER_INDEXES = set([LETTER_TO_INDEX[letter] for letter in RIGHT_LETTERS])
assert len(LEFT_LETTERS) + len(RIGHT_LETTERS) == len(LETTER_COORDS)

# todo: get better numbers
SIMULTANEOUS_LATENCY_MS = 30
MOVEMENT_LATENCY_MS = 15

BIGRAM_DICT = json.load(open("fitness/bigram_dict.json"))

def get_bigram_fitness(letter_coords, right_letters, left_letters, bigram):

    letter1 = letter_coords[0]
    letter2 = letter_coords[1]
    if letter1 in left_letters and letter2 in right_letters or letter1 in right_letters and letter2 in left_letters:
        return SIMULTANEOUS_LATENCY_MS
    else:
        # calculate distance between letters and multiply by MOVEMENT_LATENCY_MS
        distance = math.sqrt((letter1[0] - letter2[0])**2 + (letter1[1] - letter2[1])**2)
        return distance * MOVEMENT_LATENCY_MS

def get_fitness(character_sequence: str) -> float:
    # check validity of sequence
    if len(character_sequence) != len(LETTER_COORDS):
        return float('inf')
    for letter in LETTER_COORDS.keys():
        if letter not in character_sequence:
            return float('inf')
    
    # remap 

    NEW_LETTER_COORDS = {i: LETTER_COORDS[letter] for i, letter in enumerate(character_sequence)}
    NEW_RIGHT_LETTERS = set([letter for i, letter in enumerate(character_sequence) if i in RIGHT_LETTER_INDEXES])
    NEW_LEFT_LETTERS = set([letter for i, letter in enumerate(character_sequence) if i in LEFT_LETTER_INDEXES])
    # calculate fitness
    fitness = 0
    total_weight = sum(BIGRAM_DICT.values())
    for bigram, weight in BIGRAM_DICT.items():
        fitness += get_bigram_fitness(NEW_LETTER_COORDS, NEW_RIGHT_LETTERS, NEW_LEFT_LETTERS, bigram) * weight
    return fitness / total_weight

if __name__ == "__main__":
    string1 = "qwertyuiopasdfghjkl^zxcvbnm " # should work
    string2 = "qbertyuiopasdfghjkl^zxcvwnm " # should work
    string3 = "^bertyuiomasdfghjklqzxcvwnp " # should work
    string4 = "^bertyuiomasdfghjklqzxcvwnp  " # breaks
    string5 = "^bertyuiomasdfghjklzxcvwnp ]" # breaks
    string6 = "^bertyuizxcvwnp ]^" # breaks
    string7 = "qwertyuiopasdfggjkl^zxcvbnm " # should break
    print(get_fitness(string1))
    print(get_fitness(string2))
    print(get_fitness(string3))
    print(get_fitness(string4))
    print(get_fitness(string5))
    print(get_fitness(string6))
    print(get_fitness(string7))