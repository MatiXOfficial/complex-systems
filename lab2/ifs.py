import numpy as np

from ifs_common import IFSCommon


class IFS(IFSCommon):
    def __init__(self, image, W, n_jobs=1, normalize_W=True):
        if image.shape[0] != image.shape[1]:
            raise ValueError("Image must be square!")
        size = image.shape[0]

        super().__init__(W, n_jobs, size, normalize_W)

        self.points = self._find_points(image)

    def iteration(self):
        super().iteration()

        # Remove duplicates after merging the results
        if self.n_jobs > 1:
            self.points = np.unique(self.points, axis=1)

    def _find_points(self, image):
        points = []
        for x in range(self.size):
            for y in range(self.size):
                if image[x][y]:
                    points.append([x, y])

        return np.array(points).T

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
