import numpy as np


class BA:
    def __init__(self, n, m, n_start=None, compute_adj=False):
        if n_start is None:
            n_start = m
        if m > n_start:
            raise ValueError("m cannot be bigger than n_start")
        self.n = n
        self.m = m

        self.v = list(range(0, n_start))
        self.prob_num = [1] * n_start
        self.prob_den = n_start

        self.compute_adj = compute_adj
        if self.compute_adj:
            self.adj = {i: [] for i in range(n_start)}

    def turn(self):
        neighbors = self._generate_neighbors()
        self._add_vertex(neighbors)

    def build(self):
        for _ in range(self.v[-1] + 1, self.n):
            self.turn()

    def get_degrees(self):
        return np.array(self.prob_num) - 1

    def _generate_neighbors(self):
        return list(np.random.choice(self.v, size=self.m, replace=False, p=np.array(self.prob_num) / self.prob_den))

    def _add_vertex(self, neighbors):
        current_v = self.v[-1] + 1

        self.v.append(current_v)
        self.prob_num.append(self.m + 1)
        self.prob_den += self.m * 2 + 1
        if self.compute_adj:
            self.adj[current_v] = neighbors

        for n in neighbors:
            self.prob_num[n] += 1
            if self.compute_adj:
                self.adj[n].append(current_v)


if __name__ == '__main__':
    ba = BA(10, 2, 2)
    print(ba.adj)

    ba.turn()
    print(ba.adj)

    ba.turn()
    print(ba.adj)

    ba.build()
    print(ba.v)
    print(ba.adj)
    print(ba.prob_num)
