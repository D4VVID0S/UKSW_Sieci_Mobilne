from simpy import Resource, Environment
from random import random
from collections import deque
from random import seed
from functools import partial

def run_dining_philosophers(K, philosopher_process, until=None):

    # declare the environment
    table = Environment()

    # the chopsticks are a list of resources
    chopsticks = [Resource(table, capacity=1) for _ in range(K)]

    # add the philosophers processes to the environment
    for seat_no in range(K):
        table.process(philosopher_process(table, seat_no, chopsticks))

    # run the simulation
    # time=None means forever or until no more events happen,
    # that is deadlock
    table.run(until)

    return table


def philosopher(env, seat, chopsticks, loglist, max_thinking_time, eating_time, handling_time):

    my_name = f'Phil_#{seat}'

    # Determine the indexes for the left and right chopsticks for this seat
    # Example: the philosopher at seat 3 of 5 uses chopsticks 3 and 4
    L_chp_no = seat
    R_chp_no = (seat + 1) % len(chopsticks)

    while True:

        # 1-think
        thinking_time = max_thinking_time*random()
        yield env.timeout(thinking_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} is hungry!')

        # 2-grab left chopstick
        left_request = chopsticks[L_chp_no].request()
        yield left_request
        yield env.timeout(handling_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} has taken L chopstick (#{L_chp_no})')

        # 3-grab right chopstick
        right_request = chopsticks[R_chp_no].request()
        yield right_request
        yield env.timeout(handling_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} has taken R chopstick (#{R_chp_no}) and can eat')

        # 4-eat
        yield env.timeout(eating_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} is done, releases chopsticks #{L_chp_no}/#{R_chp_no}')

        # 5-release left chopstick
        yield env.timeout(handling_time)
        chopsticks[L_chp_no].release(left_request)

        # 6-release right chopstick
        yield env.timeout(handling_time)
        chopsticks[R_chp_no].release(right_request)


if __name__ == '__main__':

    # initialize the RNG used in the thinking time
    rng_seed = 12  # causes a deadlock quite early
    seed(rng_seed)

    # limited-length latest events log
    n_records = 20
    last_events_log = deque(maxlen=n_records)

    # configure the philosopher process
    p_philosopher = partial(philosopher,
                            loglist=last_events_log,
                            max_thinking_time=100,
                            eating_time=20,
                            handling_time=2)

    # run the simulation
    _ = run_dining_philosophers(
        K=5, philosopher_process=p_philosopher, until=None)

    # print the log
    [print(r) for r in last_events_log]


def philosopher_even_odd(env, seat, chopsticks, loglist, max_thinking_time, eating_time, handling_time):

    my_name = f'Phil_#{seat}'

    # Determine the indexes for the left and right chopsticks for this seat
    # Example: the philosopher at seat 3 of 5 uses chopsticks 3 and 4
    L_chp_no = seat
    R_chp_no = (seat + 1) % len(chopsticks)

    while True:

        # 1-think
        thinking_time = max_thinking_time*random()
        yield env.timeout(thinking_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} is hungry!')

        if seat % 2 == 1:
            # grab left chopstick -- only if odd
            left_request = chopsticks[L_chp_no].request()
            yield left_request
            yield env.timeout(handling_time)
            loglist.append(f'<T={env.now:.2f}>  {my_name} has taken L chopstick (#{L_chp_no})')
            conclusion = ' and can eat'
        else:
            conclusion = ''

        # grab right chopstick
        right_request = chopsticks[R_chp_no].request()
        yield right_request
        yield env.timeout(handling_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} has taken R chopstick (#{R_chp_no}){conclusion}')

        if seat % 2 == 0:
            # grab left chopstick -- only if even
            left_request = chopsticks[L_chp_no].request()
            yield left_request
            yield env.timeout(handling_time)
            loglist.append(f'<T={env.now:.2f}>  {my_name} has taken L chopstick (#{L_chp_no}) and can eat')

        # 4-eat
        yield env.timeout(eating_time)
        loglist.append(f'<T={env.now:.2f}>  {my_name} is done, releases chopsticks #{L_chp_no}/#{R_chp_no}')

        # 5-release left chopstick
        yield env.timeout(handling_time)
        chopsticks[L_chp_no].release(left_request)

        # 6-release right chopstick
        yield env.timeout(handling_time)
        chopsticks[R_chp_no].release(right_request)