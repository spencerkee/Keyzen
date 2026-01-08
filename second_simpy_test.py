import simpy
import queue


def thumb(env, q, thumb_type, my_container, other_container):
    while not q.empty():
        run = q.get()
        print(f"thumb_type={thumb_type} handling run {run} at {env.now}")
        yield other_container.get(1)
        print(
            f"thumb_type={thumb_type} got the opposite container at {env.now}, now other_container.level={other_container.level}"
        )
        yield env.timeout(len(run))
        print(f"thumb_type={thumb_type} PROCESSED {run}")
        print(
            f"thumb_type={thumb_type} Finished run={run} at {env.now}, incrementing my container, now my_container.level={my_container.level}"
        )
        yield my_container.put(1)
        print(
            f"thumb_type={thumb_type} Incremented my container, now {my_container.level} at {env.now}"
        )


right_queue = queue.Queue()
[right_queue.put(i) for i in ["jump", "mum"]]
left_queue = queue.Queue()
[left_queue.put(i) for i in ["red", "fad"]]

# jump red mum fad

env = simpy.Environment()
right_cont = simpy.Container(env, init=0, capacity=1)
left_cont = simpy.Container(env, init=1, capacity=1)

# Right thumb process
env.process(thumb(env, right_queue, "right", right_cont, left_cont))
# Left thumb process
env.process(thumb(env, left_queue, "left", left_cont, right_cont))
env.run()
