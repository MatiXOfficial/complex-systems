import numpy as np
from joblib import Parallel, delayed


class IFSCommon:
    def __init__(self, W, n_jobs, size, normalize_W=True):
        self.W = W
        self.n_jobs = n_jobs
        self.size = size

        if normalize_W:
            for w in self.W:
                w[:, 2] *= self.size

        self.points = None

    def iteration(self):
        # Handle parallel jobs
        slices = self.build_slices(self.points.shape[1], self.n_jobs)
        points = Parallel(n_jobs=self.n_jobs)(
            delayed(self._handle_points_parallel)(self.points[:, slices[i]:slices[i + 1]]) for i in
            range(len(slices) - 1))
        self.points = np.hstack(points)

    def run_iterations(self, n, log=None):
        for i in range(n):
            if log is not None:
                if i % log == 0:
                    print(f'Iteration {i}...')
            self.iteration()

    def draw_image(self):
        image = np.zeros((self.size, self.size))
        for point in self.points.T:
            x, y = int(point[0]), int(point[1])
            if 0 <= x < self.size and 0 <= y < self.size:
                image[x, y] = 1

        return image

    @staticmethod
    def build_slices(n, n_slices):
        interval = np.maximum(n // n_slices, 1)
        slices = [0]
        for _ in range(n_slices):
            slices.append(slices[-1] + interval)
            if slices[-1] >= n:
                break
        slices[-1] = n
        return slices

    def _handle_points_parallel(self, points_to_process):
        raise NotImplementedError()

    @staticmethod
    def _apply(points, w):
        return np.rint(w[:, :2] @ points + w[:, 2, None])
