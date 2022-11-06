import numpy as np

from ifs_common import IFSCommon


class RouletteIFS(IFSCommon):
    def __init__(self, W, n_points, size, n_jobs=1, P=None, normalize_W=True):
        super().__init__(np.array(W), n_jobs, size, normalize_W)
        self.P = np.array(P) if P is not None else None

        self.points = np.full((n_points, 2), [self.size // 2, self.size // 2]).T

    def _handle_points_parallel(self, points_to_process):
        w_arr = self._random_w_arr(points_to_process.shape[1])
        for i in range(points_to_process.shape[1]):
            points_to_process[:, i] = self._apply(points_to_process[:, i].reshape((-1, 1)), w_arr[i]).reshape(-1)
        return points_to_process

    def _random_w_arr(self, n):
        idx = np.random.choice(np.arange(len(self.W)), size=n, replace=True, p=self.P)
        w_arr = self.W[idx]
        return w_arr


if __name__ == '__main__':
    W = [np.array([[0.5, -0.3, 0.1], [0.5, 0, -0.02]]), np.array([[0.5, -0.1, 0.05], [0.5, 0.2, -0.15]])]
    ifs = RouletteIFS(W, 10, 100)
    ifs.iteration()
    print(ifs.points)
