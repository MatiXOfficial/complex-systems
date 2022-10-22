from queue import Queue

import numpy as np

from avalanche import Avalanche, AvalancheStats


class SimulationMap:
    def __init__(self, N: int, max_height: int = 4, neigh: str = 'default'):
        self.N = N
        self.max_height = max_height
        if neigh == 'default':
            self.neigh_method = self._newton_neigh
        elif neigh == 'moore':
            self.neigh_method = self._moore_neigh
        elif neigh == 'manhattan_2':
            self.neigh_method = self._manhattan_neigh
        else:
            raise ValueError("Wrong neighbourhood type")
        self.map = np.random.randint(low=0, high=self.max_height, size=(N, N))
        self.turn = 0
        self.stats = AvalancheStats()

    def next_turn(self, process_avalanche=True):
        self.turn += 1
        return self.add_to_random_field(process_avalanche)

    def simulate_turns(self, n_turns: int):
        for _ in range(n_turns):
            self.next_turn()

    def add_to_random_field(self, process_avalanche: bool):
        x, y = np.random.randint(low=0, high=self.N), np.random.randint(low=0, high=self.N)
        self.map[x][y] += 1
        if self.map[x][y] >= self.max_height:
            avalanche = Avalanche(self)
            self.stats.add(self.turn, avalanche)
            if process_avalanche:
                avalanche.start(x, y)
            else:
                return avalanche, (x, y)

    def collapse(self, queue: Queue = None):
        next_queue = Queue()
        next_queue_size = 0

        while not queue.empty():
            x, y = queue.get()
            # The check is required here too, in case the field is added to the queue twice
            if self.map[x][y] >= self.max_height:
                self.map[x][y] = 0
                for new_x, new_y in self.neigh_method(x, y):
                    if 0 <= new_x < self.N and 0 <= new_y < self.N:
                        self.map[new_x][new_y] += 1
                        if self.map[new_x][new_y] >= self.max_height:  # Add to the queue if more than 3
                            next_queue.put((new_x, new_y))
                            next_queue_size += 1

        return next_queue, next_queue_size

    def __str__(self):
        return str(self.map)

    @staticmethod
    def _newton_neigh(x, y):
        return [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

    @staticmethod
    def _moore_neigh(x, y):
        return SimulationMap._newton_neigh(x, y) + [(x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]

    @staticmethod
    def _manhattan_neigh(x, y):
        return SimulationMap._moore_neigh(x, y) + [(x - 2, y), (x, y + 2), (x + 2, y), (x, y - 2)]


if __name__ == '__main__':
    sim_map = SimulationMap(10)
    print(map)
    for i in range(100):
        sim_map.next_turn()
