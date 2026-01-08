import simpy
import queue
import math
import ipdb

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

LEFT_CHARS = set("qwertasdfg^zxcv")
RIGHT_CHARS = set("yuiophjklbnm ")


def create_job_queues(input_text):
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


def thumb(env, q, thumb_type, position, my_container, other_container):
    while not q.empty():
        run = q.get()
        # print(f"thumb_type={thumb_type} handling run {run} at {env.now}")
        yield other_container.get(1)
        # print(
        #     f"thumb_type={thumb_type} got the opposite container at {env.now}, now other_container.level={other_container.level}"
        # )
        distance = 0
        for char1, char2 in zip(position + run, run):
            distance += math.dist(LETTER_COORDS[char1], LETTER_COORDS[char2])
        position = run[-1]
        yield env.timeout(distance)
        print(
            f"thumb_type={thumb_type} PROCESSED run='{run}' in {distance} time units, now at {env.now}"
        )
        # print(f"thumb_type={thumb_type} PROCESSED {run}")
        # print(
        #     f"thumb_type={thumb_type} Finished run={run} at {env.now}, incrementing my container, now my_container.level={my_container.level}"
        # )
        yield my_container.put(1)
        # print(
        #     f"thumb_type={thumb_type} Incremented my container, now {my_container.level} at {env.now}"
        # )


# jump red mum fad
# left_queue, right_queue = create_job_queues("jumpredmumfad")
left_queue, right_queue = create_job_queues("jklfds")

env = simpy.Environment()
left_cont = simpy.Container(env, init=1, capacity=1)
right_cont = simpy.Container(env, init=0, capacity=1)

# Left thumb process
env.process(thumb(env, left_queue, "left", "f", left_cont, right_cont))
# Right thumb process
env.process(thumb(env, right_queue, "right", "j", right_cont, left_cont))

env.run()
