import numpy as np
from pprint import pprint
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    value: int

    def __hash__(self):
        return int(self.x * (10**6) + self.y * (10**2) + self.value)


class Day9:
    def __init__(self, filename):
        self.heightmap =[]
        with open(filename) as fd:
            for row in fd.readlines():
                self.heightmap.append(list(map(int, [char for char in row.strip()])))
        self.heightmap = np.array(self.heightmap)
        self.basins = []

    def get_min_values(self):
        min_values = []
        for y in range(len(self.heightmap)):
            for x in range(len(self.heightmap[0])):
                neighbors = self.get_neighbors(Point(x=x, y=y, value=self.heightmap[y][x]))
                if all(self.heightmap[y][x] < neighbor.value for neighbor in neighbors):
                    min_values.append(Point(x=x, y=y, value=self.heightmap[y][x]))
        return min_values

    def solve_1(self):
        return sum(x['value'] + 1 for x in self.get_min_values())

    def solve_2(self):
        for stationary_point in self.get_min_values():
            self.get_basin_around(stationary_point)
        self.basins.sort(key=lambda x: -len(x))
        return len(self.basins[0]) * len(self.basins[1]) * len(self.basins[2])

    def get_neighbors(self, point):
        x = point.x
        y = point.y
        neighbors = []
        if y - 1 >= 0:
            neighbors.append(Point(x=x, y=y-1, value=self.heightmap[y - 1][x]))
        if y + 1 < len(self.heightmap):
            neighbors.append(Point(x=x, y=y+1, value=self.heightmap[y + 1][x]))
        if x - 1 >= 0:
            neighbors.append(Point(x=x-1, y=y, value=self.heightmap[y][x - 1]))
        if x + 1 < len(self.heightmap[0]):
            neighbors.append(Point(x=x+1, y=y, value=self.heightmap[y][x + 1]))
        return neighbors

    def get_basin_around(self, stationary_point):
        self.basins.append(set([stationary_point]))
        neighbors = self.get_neighbors(stationary_point)
        [self.basins[-1].add(neighbor) for neighbor in neighbors if neighbor.value != 9]
        for neighbor in neighbors:
            if neighbor.value != 9:
                self.search_for_new_basin_points_around(neighbor)

    def search_for_new_basin_points_around(self, point):
        neighbors = self.get_neighbors(point)
        added_neighbors = []
        for neighbor in neighbors:
            if neighbor not in self.basins[-1] and neighbor.value != 9:
                added_neighbors.append(neighbor)
                self.basins[-1].add(neighbor)

        if not added_neighbors:
            return False

        for neighbor in added_neighbors:
            self.search_for_new_basin_points_around(neighbor)


def main():
    pprint(Day9('input.txt').solve_1())
    pprint(Day9('input_01.txt').solve_1())
    pprint(Day9('input.txt').solve_2())
    pprint(Day9('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
