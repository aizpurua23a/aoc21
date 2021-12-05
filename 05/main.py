from pprint import pprint
from dataclasses import dataclass
import numpy as np


@dataclass
class Segment:
    start: tuple
    end: tuple
    is_ortho: bool


class Day5:
    def __init__(self, filename):
        self.segments = []
        max_coord = 0

        with open(filename) as file:
            for idx, line in enumerate(file.readlines()):
                x1_y1, x2_y2 = line.strip().split(' -> ')
                x1, y1 = map(int, x1_y1.split(','))
                x2, y2 = map(int, x2_y2.split(','))
                self.segments.append(Segment(start=(x1, y1), end=(x2, y2), is_ortho=bool(x1 == x2 or y1 == y2)))
                max_coord = max(x1, y1, x2, y2, max_coord)
        self.grid = np.zeros((max_coord+1, max_coord+1), dtype=int)

    def get_step(self, a0, a1):
        return int((a1-a0)/abs(a1-a0) if a1 != a0 else 0)

    def add_segments_to_grid(self, grid, limit_to_orthos=False):
        for segment in self.segments:
            x_end = segment.end[0] + (1 if segment.start[0] < segment.end[0] else -1)
            x_step = self.get_step(segment.start[0], segment.end[0])
            y_end = segment.end[1] + (1 if segment.start[1] < segment.end[1] else -1)
            y_step = self.get_step(segment.start[1], segment.end[1])
            if limit_to_orthos and x_step != 0 and y_step != 0:
                continue
            for idx in range(max(abs(x_end - segment.start[0]), abs(y_end - segment.start[1]))):
                x = segment.start[0] + idx * x_step
                y = segment.start[1] + idx * y_step
                grid[x][y] += 1
        return grid

    def solve_1(self):
        output_grid = self.add_segments_to_grid(self.grid, limit_to_orthos=True)
        self.sum_grid = np.array([[x if x >= 2 else 0 for x in row] for row in output_grid])
        pprint(np.count_nonzero(self.sum_grid))

    def solve_2(self):
        output_grid = self.add_segments_to_grid(self.grid)
        self.sum_grid = np.array([[x if x >= 2 else 0 for x in row] for row in output_grid])
        pprint(np.count_nonzero(self.sum_grid))


def main():
    Day5('input.txt').solve_1()
    Day5('input.txt').solve_2()


if __name__ == '__main__':
    main()
