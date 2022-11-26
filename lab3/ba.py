import numpy as np


class BA:
    def __init__(self, n, m, n_start=None, compute_adj=False):
        if n_start is None:
            n_start = m
        if m > n_start:
            raise ValueError("m cannot be bigger than n_start")
        self.n = n
        self.m = m

        self.next_v = n_start
        self.v_list = np.arange(self.n)

        self.prob_num = np.zeros(self.n)
        self.prob_num[:n_start] = 1
        self.prob_den = n_start

        self.adj = None
        self.compute_adj = compute_adj
        if self.compute_adj:
            self.adj = {i: [] for i in range(n_start)}

    def turn(self):
        neighbors = self._generate_neighbors()
        self._add_vertex(neighbors)

    def build(self):
        for _ in range(self.next_v, self.n):
            self.turn()

    def get_degrees(self):
        return self.prob_num - 1

    def _generate_neighbors(self):
        return np.random.choice(self.v_list[:self.next_v], size=self.m, replace=False,
                                p=self.prob_num[:self.next_v] / self.prob_den)

    def _add_vertex(self, neighbors):
        self.prob_num[self.next_v] = self.m + 1
        self.prob_den += self.m * 2 + 1
        if self.compute_adj:
            self.adj[self.next_v] = list(neighbors)

        for n in neighbors:
            self.prob_num[n] += 1
            if self.compute_adj:
                self.adj[n].append(self.next_v)

        self.next_v += 1


if __name__ == '__main__':
    ba = BA(10, 2, 2, compute_adj=True)
    print(ba.adj)

    ba.turn()
    print(ba.adj)

    ba.turn()
    print(ba.adj)

    ba.build()
    print(ba.next_v)
    print(ba.adj)
    print(ba.prob_num)
    print(ba.get_degrees())
