'''
Zespół:
Agata Wąsik
Magda Sarełło
Maciej Nachtygal
Matteo Dawide Catalani
'''

import threading
import random
import time

# inheriting threading class in Thread module
class Philosopher(threading.Thread):
    running = True  # used to check if everyone is finished eating

    start_time = time.time()  # Starting time for the dining process

    # Since the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.
    def __init__(self, index, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.index = index
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
        self.attempts = 0
        self.eating_time = 0

    def run(self):
        while self.running:
            # Philosopher is thinking (but really is sleeping).
            thinking_time = random.randint(1, 5)  # Randomize thinking time between 1 and 5 seconds
            time.sleep(thinking_time)
            print('[%s] Philosopher %s is hungry.' % (self.get_elapsed_time(), self.index))
            self.dine()

    def dine(self):
        # if both the semaphores(forks) are free, then philosopher will eat
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
        while self.running:
            fork1.acquire()  # wait operation on left fork
            locked = fork2.acquire(False)
            if locked:
                break  # if right fork is not available, leave left fork
            self.attempts += 1
            fork1.release()
            print('[%s] Philosopher %s swaps forks.' % (self.get_elapsed_time(), self.index))
            fork1, fork2 = fork2, fork1
        else:
            return
        self.dining()
        # release both the forks after dining
        fork2.release()
        fork1.release()

    def dining(self):
        print('[%s] Philosopher %s starts eating.' % (self.get_elapsed_time(), self.index))
        eating_time = random.randint(1, 5)  # Randomize eating time between 1 and 5 seconds
        start_time = time.time()  # Start time for eating
        time.sleep(eating_time)
        end_time = time.time()  # End time for eating
        self.eating_time += (end_time - start_time)
        print('[%s] Philosopher %s finishes eating and leaves to think.' % (self.get_elapsed_time(), self.index))
        print('[%s] Philosopher %s ate for %.2f seconds.' % (self.get_elapsed_time(), self.index, end_time - start_time))
        print('[%s] Philosopher %s attempted to eat %d time(s) before successfully eating.' % (self.get_elapsed_time(), self.index, self.attempts))

    def get_elapsed_time(self):
        elapsed_time = int(time.time() - self.start_time) 
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def main():
    forks = [threading.Semaphore() for _ in range(5)]  # initializing array of semaphores i.e. forks

    # here (i+1)%5 is used to get right and left forks circularly between 1-5
    philosophers = [Philosopher(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]

    Philosopher.running = True

    for p in philosophers:
        p.start()

    time.sleep(10)
    Philosopher.running = False

    for p in philosophers:
        p.join()  # Wait for all philosophers to finish

    end_time = time.time()  # End time for the dining process
    total_time = end_time - Philosopher.start_time
    print("Now we're finishing.")
    print("Total dining time: %.2f seconds" % total_time)

if __name__ == "__main__":
    main()
