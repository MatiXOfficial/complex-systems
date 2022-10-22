from queue import Queue

import numpy as np


class Avalanche:
    def __init__(self, map_):
        self.map = map_
        self.size = 0
        self.duration = 0

    def process_queue(self, queue: Queue, queue_size: int):
        self.size += queue_size
        self.duration += 1
        return self.map.collapse(queue)

    def start(self, x, y, return_map_states=False):
        if return_map_states:
            map_states = [np.copy(self.map.map)]
        queue = Queue()
        queue.put((x, y))

        queue_size = 1
        while not queue.empty():
            queue, queue_size = self.process_queue(queue, queue_size)
            if return_map_states:
                map_states.append(np.copy(self.map.map))

        if return_map_states:
            return map_states

    def reset(self):
        self.size = 0
        self.duration = 0


class AvalancheStats:
    def __init__(self):
        self.avalanches: list[Avalanche] = []
        self.times: list[int] = []

    def add(self, turn: int, avalanche: Avalanche):
        self.avalanches.append(avalanche)
        self.times.append(turn)

    def get_sizes(self):
        return np.array([a.size for a in self.avalanches])

    def get_durations(self):
        return np.array([a.duration for a in self.avalanches])

    def get_times(self):
        return np.array(self.times)
