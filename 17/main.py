from pprint import pprint

class Day17:
    def __init__(self, filename):
        with open(filename) as fd:
            string_limits = fd.read().strip().split('target area: ')[1]
            x_str, y_str = string_limits.split(' ')
            self.x_min, self.x_max = list(map(int, [char for char in x_str.split('x=')[1].split(',')[0].split('..')]))
            self.y_min, self.y_max = list(map(int, [char for char in y_str.split('y=')[1].split('..')]))

        self.initial_pos = [0, 0]

    def solve_1(self):
        return max(v[1] for v in self._get_valid_velocities())

    def solve_2(self):
        return len(self._get_valid_velocities())

    def _get_valid_velocities(self):
        valid_velocities = []
        for v0_x in range(300):
            for v0_y in range(-300, 300):
                p = [0, 0]
                v = [v0_x, v0_y]
                oob = False
                point_history = []
                point_history.append(p.copy())

                while not oob:
                    p, v = self._calculate_step(p, v)
                    point_history.append(p.copy())
                    if p[0] > self.x_max or p[1] < self.y_min:
                        oob = True

                if self._any_point_in_target_area(point_history):
                    valid_velocities.append([[v0_x, v0_y], self._get_highest_position_in_point_history(point_history)])

        return valid_velocities

    def _any_point_in_target_area(self, point_history):
        for point in point_history:
            if self.x_min <= point[0] <= self.x_max:
                if self.y_min <= point[1] <= self.y_max:
                    return True
        return False

    def _get_highest_position_in_point_history(self, point_history):
        return max(p[1] for p in point_history)

    def _calculate_step(self, p, v):
        p[0] += v[0]
        p[1] += v[1]

        if v[0] > 0:
            v[0] -= 1
        elif v[0] < 0:
            v[0] += 1
        else:
            v[0] = 0

        v[1] -= 1

        return p, v


def main():
    print(Day17('input.txt').solve_1())
    print(Day17('input_01.txt').solve_1())
    print(Day17('input.txt').solve_2())
    print(Day17('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
