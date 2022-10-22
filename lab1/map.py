import numpy as np

from queue import Queue

from avalanche import Avalanche, AvalancheStats

class Map:
    def __init__(self, N):
        self.N = N
        self.map = np.random.randint(low=0, high=4, size=(N, N))
        self.turn = 0
        self.avalanche_stats = AvalancheStats()

    def next_turn(self):
        self.turn += 1
        self.add_to_random_field()

    def add_to_random_field(self):
        x, y = np.random.randint(low=0, high=self.N), np.random.randint(low=0, high=self.N)
        self.map[x][y] += 1
        if self.map[x][y] >= 4:
            avalanche = Avalanche(self)
            avalanche.start(x, y)
            self.avalanche_stats.add(avalanche, self.turn)

    def collapse(self, queue: Queue = None):
        next_queue = Queue()
        next_queue_size = 0

        while not queue.empty():
            x, y = queue.get()
            # The check is required here too, in case of adding a field to the queue twice
            if self.map[x][y] >= 4: 
                self.map[x][y] = 0
                for new_x, new_y in [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]:
                    if new_x >= 0 and new_x < self.N and new_y >= 0 and new_y < self.N:
                        self.map[new_x][new_y] += 1
                        if self.map[new_x][new_y] >= 4: # Add to the queue if more than 3
                            next_queue.put((new_x, new_y))
                            next_queue_size += 1

        return next_queue, next_queue_size

    def __str__(self):
        return str(self.map)

if __name__ == '__main__':
    map = Map(10)
    print(map)
    for i in range(100):
        map.next_turn()
