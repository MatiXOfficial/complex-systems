from queue import Queue


class Avalanche:
    def __init__(self, map):
        self.map = map
        self.size = 0
        self.duration = 0

    def start(self, x, y):
        queue = Queue()
        queue.put((x, y))

        queue_size = 1
        while not queue.empty():
            self.size += queue_size
            self.duration += 1
            queue, queue_size = self.map.collapse(queue)


class AvalancheStats:
    def __init__(self):
        self.avalanches_turn_dict = {}

        self.avalanche_sizes = []
        self.avalanche_durations = []

    def add(self, avalanche: Avalanche, turn: int):
        self.avalanches_turn_dict[turn] = avalanche
        self.avalanche_sizes.append(avalanche.size)
        self.avalanche_durations.append(avalanche.duration)

