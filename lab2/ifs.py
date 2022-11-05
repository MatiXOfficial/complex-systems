import numpy as np

class IFS:
    def __init__(self, image, W) -> None:
        self.W = W

        self.n_rows = image.shape[0]
        self.n_cols = image.shape[1]
        self.points = self._find_points(image)

    def iteration(self):
        self.points = np.rint(self.W[:, :2] @ self.points.T)

    def draw_image(self):
        image = np.zeros((self.n_rows, self.n_cols))
        for point in self.points.T:
            x, y = int(point[0]), int(point[1])
            # print(x, y)
            if x >= 0 and x < self.n_rows and y >= 0 and y < self.n_cols:
                image[x, y] = 1

        return image

    def _find_points(self, image):
        points = []
        for x in range(self.n_rows):
            for y in range(self.n_cols):
                if image[x][y]:
                    points.append([x, y])

        return np.array(points)

    def _apply(self, x, y):
        point = self.W[:, :2] @ np.array([x, y]) + self.W[:, 2]
        return int(point[0]), int(point[1])


if __name__ == '__main__':
    image = np.zeros((100, 100))
    image[50, 50] = 1
    image[25, 25] = 1

    W = np.array([
        [0.5, -0.4, 0],
        [0.5, 0, 0]
    ])

    ifs = IFS(image, W)
    ifs.iteration()
    ifs.iteration()
    ifs.draw_image()
