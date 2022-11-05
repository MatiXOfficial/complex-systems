import numpy as np
from joblib import Parallel, delayed


class IFS:
    def __init__(self, image, W, n_jobs=1, normalize_W=True):
        self.W = W
        self.n_jobs = n_jobs

        if image.shape[0] != image.shape[1]:
            raise ValueError("Image must be square!")

        self.size = image.shape[0]
        self.points = self._find_points(image)

        if normalize_W:
            for w in self.W:
                w[:, 2] *= self.size

    def iteration(self):
        # Handle parallel jobs
        slices = self._build_slices(self.points.shape[1], self.n_jobs)
        points = Parallel(n_jobs=self.n_jobs)(
            delayed(self._handle_points_parallel)(self.points[:, slices[i]:slices[i + 1]]) for i in
            range(len(slices) - 1))
        self.points = np.hstack(points)

        # Remove duplicates after merging the results
        if self.n_jobs > 1:
            self.points = np.unique(self.points, axis=1)

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

    def _find_points(self, image):
        points = []
        for x in range(self.size):
            for y in range(self.size):
                if image[x][y]:
                    points.append([x, y])

        return np.array(points).T

    @staticmethod
    def _build_slices(n, n_slices):
        interval = np.maximum(n // n_slices, 1)
        slices = [0]
        for _ in range(n_slices):
            slices.append(slices[-1] + interval)
            if slices[-1] >= n:
                break
        slices[-1] = n
        return slices

    def _handle_points_parallel(self, points_to_process):
        # Apply contractions
        points = []
        for w in self.W:
            points.append(self._apply(points_to_process, w))
        points = np.hstack(points)

        # Remove duplicates
        points = np.unique(points, axis=1)

        # Remove wrong points
        cond = np.logical_and(np.all(points >= 0, axis=0), np.all(points < self.size, axis=0))
        return points[:, cond]

    @staticmethod
    def _apply(points, w):
        return np.rint(w[:, :2] @ points + w[:, 2, None])


if __name__ == '__main__':
    image = np.zeros((100, 100))
    image[50, 50] = 1
    image[25, 25] = 1
    image[75, 80] = 1
    image[76, 80] = 1
    image[0, 50] = 1

    W = [np.array([[0.5, -0.3, 0.1], [0.5, 0, -0.02]])]

    ifs = IFS(image, W, n_jobs=2)
    print('0\n', ifs.points)
    ifs.iteration()
    print('1\n', ifs.points)
    ifs.iteration()
    print('2\n', ifs.points)

    ifs.draw_image()
