"""
Simpy demo showing how to dynamicaly chain
together tasks to make a process.

a task can have more then one pressedent
and the task will wait for all pressedents to
finish before starting

programmer: Michael R. Gibbs
"""

import simpy
import itertools
import math
from pprint import pprint

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


def make_distance_matrix(letter_coords):
    ret = {}
    for (letter1, letter1coords), (letter2, letter2coords) in itertools.combinations(
        letter_coords.items(), 2
    ):
        ret[letter1 + letter2] = math.dist(letter1coords, letter2coords)
        ret[letter2 + letter1] = math.dist(letter1coords, letter2coords)
    return ret


DIST_MATRIX = make_distance_matrix(LETTER_COORDS)

LEFT_CHARS = set("qwertasdfg^zxcv")

RIGHT_CHARS = set("yuiophjklbnm ")

INPUT_TEXT = """quite"""


def create_jobs_data(input_text):
    last_left = "f"
    last_left_ind = None
    last_right = "j"
    last_right_ind = None
    jobs_data = []
    for ind, char in enumerate(input_text):
        if char in LEFT_CHARS:
            job_id = "left_job"
            hand_required = "left"
            distance = DIST_MATRIX[last_left + char]
            last_left = char
            last_left_ind = ind
        else:
            job_id = "right_job"
            hand_required = "right"
            distance = DIST_MATRIX[last_right + char]
            last_right = char
            last_right_ind = ind
        task_id = ind
        time = 0
        next_task = 0
        jobs_data.append([job_id, task_id, hand_required, distance, ind + 1])
    if last_left_ind is not None:
        jobs_data[last_left_ind][4] = -1
    if last_right_ind is not None:
        jobs_data[last_right_ind][4] = -1

    return jobs_data


jobs_data = create_jobs_data(INPUT_TEXT)

# each machine type has it own resource pool
# This allows testing the addition of
# machines to relieve a bottle necks
machine_pools_data = [
    # machine name, qty
    ["left", 1],
    ["right", 1],
]

# defines a job made up of tasks
# each task uses a machine for x amount of time
# and it output goes to a next task.
# jobs_data = [
#     # job id, task id, machine, time, next task
#     ["p1", 1, "a1", 17, 2],
#     ["p1", 2, "a2", 30, 4],
#     ["p1", 3, "a3", 14, 4],
#     ["p1", 4, "a4", 15, 5],
#     ["p1", 5, "a5", 25, -1],
#     ["p2", 1, "a1", 13, 3],
#     ["p2", 2, "a3", 15, 3],
#     ["p2", 3, "a2", 10, 4],
#     ["p2", 4, "a6", 20, -1],
# ]


def task(env, job_id, task_id, machine_pool, time, precedent_tasks):
    """
    hart of the processing

    waits for the completions of pressidenct tasks (list can be empty)
    grabs a resouce
    spend some time doing the task
    """

    print(f"{env.now}, job: {job_id}, task_id: {task_id}, waitting for pressedents")

    yield env.all_of(precedent_tasks)

    print(f"{env.now}, job: {job_id}, task_id: {task_id}, getting resource")
    with machine_pool.request() as req:

        yield req

        print(f"{env.now}, job: {job_id}, task_id: {task_id}, starting task")

        yield env.timeout(time)

    print(f"{env.now}, job: {job_id}, task_id: {task_id}, finished task")


def build_pools(env, pool_data):
    """
    builds a dict of resouces pools from data

    index 0: name of machine type
    index 1: number of machines in the pool
    """

    pools = {}

    for pool in pool_data:
        pools[pool[0]] = simpy.Resource(env, capacity=pool[1])

    return pools


def build_jobs(env, pools, job_data):
    """
    builds a tree of tasks where the root node
    is the exit of the job, and leaf nodes
    start the job.  leaf nodes have no pressidents
    there can be more then one leaf node.
    there can only be one root node
    """

    jobs = {}

    # prime the node tree with default empty nodes
    for job in job_data:
        tasks = jobs.setdefault(job[0], {})
        tasks[job[1]] = []

        if job[4] < 0:
            # add exit node
            tasks[-1] = []

    # fill in pressedents for each node
    # leaf nodes end with empty pressident lists
    pprint(tasks)
    for job in job_data:
        print(f"job={job}")
        job_id = job[0]
        print(f"job_id={job_id}")
        tasks = jobs[job_id]  # tasks for job
        print(f"tasks={tasks}")
        next_task = job[4]
        print(f"next_task={next_task}")
        press = tasks[next_task]  # get pressident list for task
        press.append(job)  # add pressedent node data

    # start a recursive process that
    # walks the node tree, creating the tasks
    for job in jobs.keys():
        tasks = jobs[job]

        exit_node = tasks[-1][0]

        build_tasks(env, tasks, exit_node, pools)


def build_tasks(env, tasks, node, pools):
    """
    recurse down the pressidents and work from the
    leafs back creating tasks, which are used as
    pressident events for the parent node.
    """

    press_tasks = []

    press_nodes = tasks[node[1]]  # get list of pressident nodes

    # recurse the pressidents to get task processes that
    # this node can use to wait on.
    for press_node in press_nodes:
        press_tasks.append(build_tasks(env, tasks, press_node, pools))

    # create the task process
    t = task(env, node[0], node[1], pools[node[2]], node[3], press_tasks)

    # retrun the process to the parent, which the parent
    # will wait on as a pressident
    t = env.process(t)

    return t


# boot up
env = simpy.Environment()

pools = build_pools(env, machine_pools_data)

build_jobs(env, pools, jobs_data)

env.run(100)

print("done")
