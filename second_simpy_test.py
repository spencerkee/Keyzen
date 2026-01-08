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
    (2.5, 2),
    (3.5, 2),
    (4.5, 2),
    (5.5, 2),
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
CHARACTER_SET = set("qwertyuiopasdfghjkl^zxcvbnm ")


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
        if char in LEFT_CHARS:
            if current_thumb == "right":
                right_queue.put(current_run)
                current_run = ""
            current_thumb = "left"
            current_run += char
        elif char in RIGHT_CHARS:
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


if __name__ == "__main__":

    # CHROMOSOME = "qwertyuiopasdfghjkl^zxcvbnm " # QWERTY 6608.455772598619
    CHROMOSOME = (
        "qwertyuiopasdfgh kl^zxcvbnmj"  # J and space swapped, 5028.270082811743
    )
    LEFT_CHARS = set((CHROMOSOME[i] for i in LEFT_LETTERS))
    RIGHT_CHARS = set((CHROMOSOME[i] for i in RIGHT_LETTERS))
    LETTER_COORDS = {char: COORDS[i] for i, char in enumerate(CHROMOSOME)}

    # jump red mum fad
    # left_queue, right_queue = create_job_queues("jumpredmumfad")
    input_text = preprocess_input_text(TEXT_INPUT)
    left_queue, right_queue = create_job_queues(input_text, LEFT_CHARS, RIGHT_CHARS)

    env = simpy.Environment()
    # TODO Start with the correct container.
    left_cont = simpy.Container(env, init=1, capacity=1)
    right_cont = simpy.Container(env, init=0, capacity=1)

    # TODO Start with the correct position of the thumbs.
    # Left thumb process
    env.process(
        thumb(env, left_queue, "left", "f", left_cont, right_cont, LETTER_COORDS)
    )
    # Right thumb process
    env.process(
        thumb(env, right_queue, "right", "j", right_cont, left_cont, LETTER_COORDS)
    )

    env.run()
    print(f"Final environment time: {env.now}")
