from enum import Enum

import numpy as np

from ba import BA


class RemoveMode(Enum):
    RANDOM = 0
    ATTACK = 1


class BARemover(BA):
    def __init__(self, n, m, n_start=None, remove_mode='random'):
        super().__init__(n, m, n_start, compute_adj=True)

        if remove_mode == 'random':
            self.remove_mode = RemoveMode.RANDOM
            self.remove_vertex = self._remove_random
        elif remove_mode == 'attack':
            self.remove_mode = RemoveMode.ATTACK
            self.remove_vertex = self._remove_attack
        else:
            raise ValueError('Wrong remove mode')

    def build(self):
        super().build()
        if self.remove_mode == RemoveMode.RANDOM:
            self.v_list = set(self.v_list)
            self.prob_num = {u: self.prob_num[u] for u in range(self.n)}

    def _remove_random(self):
        u = np.random.choice(list(self.v_list))
        self._remove_vertex(u)

    def _remove_attack(self):
        u = np.random.choice(self.v_list, p=self.prob_num / self.prob_den)
        self._remove_vertex(u)

    def _remove_vertex(self, u):
        for v in self.adj[u]:
            self.adj[v].remove(u)
            self.prob_num[v] -= 1
            if not self.adj[v]:  # Remove v if it has no edges
                self._remove_vertex(v)

        self.prob_den -= self.prob_num[u] * 2 - 1
        del self.adj[u]

        if self.remove_mode == RemoveMode.RANDOM:
            self.v_list.remove(u)
            del self.prob_num[u]
        elif self.remove_mode == RemoveMode.ATTACK:
            self.prob_num[u] = 0


if __name__ == '__main__':
    ba = BARemover(10, 2, remove_mode='random')
    ba.build()

    print(ba.adj)
    ba.remove_vertex()
    print(ba.adj)
    ba.remove_vertex()
    ba.remove_vertex()
    print(ba.adj)

    print('--------------------------------------------')
    ba = BARemover(10, 2, remove_mode='attack')
    ba.build()

    print(ba.adj)
    ba.remove_vertex()
    print(ba.adj)
    ba.remove_vertex()
    ba.remove_vertex()
    print(ba.adj)
