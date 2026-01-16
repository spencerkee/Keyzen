import simpy
import queue
import math
import ipdb
import re
from simpy_keyboard import TEXT_INPUT

COORDS = (
    (0, 3),
    (1, 3),
    (2, 3),
    (3, 3),
    (4, 3),
    (5, 3),
    (6, 3),
    (7, 3),
    (8, 3),
    (9, 3),
    (0.5, 2),
    (1.5, 2),
    (2.5, 2),  # f
    (3.5, 2),
    (4.5, 2),
    (5.5, 2),  # j
    (6.5, 2),
    (7.5, 2),
    (8.5, 2),
    (0, 1),
    (1.5, 1),
    (2.5, 1),
    (3.5, 1),
    (4.5, 1),
    (5.5, 1),
    (6.6, 1),
    (7.5, 1),
    (5.5, 0),
)
LEFT_LETTERS = set([0, 1, 2, 3, 4, 10, 11, 12, 13, 19, 20, 21, 22])
RIGHT_LETTERS = set([5, 6, 7, 8, 9, 15, 16, 17, 18, 24, 25, 26, 27])
CHARACTERS = "qwertyuiopasdfghjkl^zxcvbnm "
CHARACTER_SET = set(CHARACTERS)


def insert_char_before_capitals(text, char_to_insert="^"):
    """
    Inserts a specified character before every capital letter in a string.

    Args:
      text: The original string.
      char_to_insert: The character (or string) to insert.

    Returns:
      The modified string.
    """
    # The pattern '([A-Z])' captures any uppercase letter.
    # The replacement uses a backreference '\\1' to refer to the captured letter,
    # inserting the specified character before it.
    return re.sub(r"([A-Z])", char_to_insert + r"\1", text)


def preprocess_input_text(input_text):
    # Insert '^' before capital letters and lowercase the entire string
    input_text = insert_char_before_capitals(input_text)
    input_text = input_text.lower()
    # Remove characters that are not in the CHARACTER_SET
    input_text = "".join(char for char in input_text if char in CHARACTER_SET)
    return input_text


def create_job_queues(input_text, left_chars, right_chars):
    left_queue = queue.Queue()
    right_queue = queue.Queue()
    # Iterate through the input text and add runs of characters typed by the same thumb to the respective queues
    current_thumb = None
    current_run = ""
    for char in input_text:
        if char in left_chars:
            if current_thumb == "right":
                right_queue.put(current_run)
                current_run = ""
            current_thumb = "left"
            current_run += char
        elif char in right_chars:
            if current_thumb == "left":
                left_queue.put(current_run)
                current_run = ""
            current_thumb = "right"
            current_run += char
    # Add any remaining run to the respective queue
    if current_run:
        if current_thumb == "left":
            left_queue.put(current_run)
        else:
            right_queue.put(current_run)
    return left_queue, right_queue


def thumb(env, q, thumb_type, position, my_container, other_container, letter_coords):
    while not q.empty():
        run = q.get()
        # print(f"thumb_type={thumb_type} handling run {run} at {env.now}")
        yield other_container.get(1)
        # print(
        #     f"thumb_type={thumb_type} got the opposite container at {env.now}, now other_container.level={other_container.level}"
        # )
        distance = 0
        for char1, char2 in zip(position + run, run):
            distance += math.dist(letter_coords[char1], letter_coords[char2])
        position = run[-1]
        yield env.timeout(distance)
        # print(
        #     f"thumb_type={thumb_type} PROCESSED run='{run}' in {distance} time units, now at {env.now}"
        # )
        # print(f"thumb_type={thumb_type} PROCESSED {run}")
        # print(
        #     f"thumb_type={thumb_type} Finished run={run} at {env.now}, incrementing my container, now my_container.level={my_container.level}"
        # )
        yield my_container.put(1)
        # print(
        #     f"thumb_type={thumb_type} Incremented my container, now {my_container.level} at {env.now}"
        # )


# Chromosome can be a string or a list (hopefully this won't come back to bite me).
def get_distance_for_chromosome(chromosome, preprocessed_input_text):
    # Chromosome is a list of indices (technically deap.creator.Individual),
    # so we need to convert it to characters.
    if type(chromosome) != str:
        individual_as_characters = [CHARACTERS[i] for i in chromosome]
        chromosome = "".join(individual_as_characters)
    left_chars = set((chromosome[i] for i in LEFT_LETTERS))
    right_chars = set((chromosome[i] for i in RIGHT_LETTERS))
    letter_coords = {char: COORDS[i] for i, char in enumerate(chromosome)}

    # left_queue, right_queue = create_job_queues("jumpredmumfad")
    left_queue, right_queue = create_job_queues(
        preprocessed_input_text, left_chars, right_chars
    )

    env = simpy.Environment()
    # TODO Start with the correct container.
    left_cont = simpy.Container(env, init=1, capacity=1)
    right_cont = simpy.Container(env, init=0, capacity=1)

    # TODO Start with the correct position of the thumbs.
    # Left thumb process

    # Equivalent to the positions of F and J on qwerty.
    left_starting_letter = chromosome[12]
    right_starting_letter = chromosome[15]
    env.process(
        thumb(
            env,
            left_queue,
            "left",
            left_starting_letter,
            left_cont,
            right_cont,
            letter_coords,
        )
    )
    # Right thumb process
    env.process(
        thumb(
            env,
            right_queue,
            "right",
            right_starting_letter,
            right_cont,
            left_cont,
            letter_coords,
        )
    )

    env.run()
    # print(f"Final environment time: {env.now}")
    # Fitness values must be iterable because single fitness functions
    # are a special case of multi-fitness functions.
    # https://deap.readthedocs.io/en/master/overview.html#operators
    return (env.now,)


def predict_distance_for_chromosome(chromosome):
    # Chromosome is a list of 28 indices.
    # Create numpy array where each element corresponds to every pair (i,j) to indicate if i appears before j in the permutation.
    n = len(chromosome)
    pairwise_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            pairwise_matrix[chromosome[i], chromosome[j]] = 1
    return pairwise_matrix


if __name__ == "__main__":

    # # CHROMOSOME = "qwertyuiopasdfghjkl^zxcvbnm " # QWERTY 6608.455772598619
    # CHROMOSOME = (
    #     "qwertyuiopasdfgh kl^zxcvbnmj"  # J and space swapped, 5028.270082811743
    # )
    # preprocess_input_text = preprocess_input_text(TEXT_INPUT)
    # get_distance_for_chromosome(CHROMOSOME, preprocess_input_text)

    # from autogluon.tabular import TabularDataset, TabularPredictor

    # data_url = "https://raw.githubusercontent.com/mli/ag-docs/main/knot_theory/"
    # train_data = TabularDataset(f"{data_url}train.csv")
    # train_data.head()
    # label = "signature"
    # train_data[label].describe()
    # predictor = TabularPredictor(label=label).fit(train_data)
    # test_data = TabularDataset(f"{data_url}test.csv")

    # y_pred = predictor.predict(test_data.drop(columns=[label]))
    # y_pred.head()
    # predictor.evaluate(test_data)
    # predictor.leaderboard(test_data)
