import numpy as np


class Day15AltAlt:
    def __init__(self, filename):
        with open(filename) as fd:
            matrix = []
            for row in fd.readlines():
                matrix.append(list(map(int, row.strip())))
        self.matrix = np.array(matrix)

    def solve_2(self):
        row_matrices = [np.concatenate([self.get_updated_matrix(self.matrix, col_step + row_step)
                                        for row_step in range(5)], axis=1) for col_step in range(5)]
        return self.get_optimal_sum_matrix(np.concatenate(row_matrices, axis=0))[-1][-1]

    def solve_1(self):
        return self.get_optimal_sum_matrix(self.matrix)[-1][-1]

    def get_updated_matrix(self, matrix, step):
        return np.vectorize(lambda x: (x-1+step) % 9+1)(matrix)

    def get_optimal_sum_matrix(self, matrix):
        max_y, max_x = np.size(matrix, 0), np.size(matrix, 1)

        sum_matrix = []
        for idy, row in enumerate(matrix):
            sum_matrix.append([])
            for idx, value in enumerate(row):
                if idy == 0 and idx == 0:
                    sum_matrix[idy].append(0)
                    continue

                if idx == 0:
                    sum_matrix[idy].append(sum_matrix[idy - 1][0] + matrix[idy][idx])
                    continue
                sum_matrix[idy].append(sum_matrix[idy][idx - 1] + matrix[idy][idx])

        _pass = 0
        changes = 1
        while changes:
            changes = 0
            for idy in range(max_y):
                for idx in range(max_x):
                    sum_matrix, step_change = self.update_sum_matrix(idy, idx, matrix, sum_matrix)
                    if step_change:
                        changes += 1

            print(f'Pass {_pass}, changes {changes}.')
            _pass += 1
        return sum_matrix

    def update_sum_matrix(self, idy, idx, matrix, sum_matrix):
        max_y = np.size(matrix, 0)
        max_x = np.size(matrix, 1)
        step_change = False

        if idy > 0:
            if sum_matrix[idy][idx] + matrix[idy-1][idx] < sum_matrix[idy-1][idx]:
                sum_matrix[idy-1][idx] = sum_matrix[idy][idx] + matrix[idy-1][idx]
                step_change = True

        if idx > 0:
            if sum_matrix[idy][idx] + matrix[idy][idx-1] < sum_matrix[idy][idx-1]:
                sum_matrix[idy][idx-1] = sum_matrix[idy][idx] + matrix[idy][idx-1]
                step_change = True

        if idy < max_y-1:
            if sum_matrix[idy][idx] + matrix[idy+1][idx] < sum_matrix[idy+1][idx]:
                sum_matrix[idy+1][idx] = sum_matrix[idy][idx] + matrix[idy+1][idx]
                step_change = True

        if idx < max_x-1:
            if sum_matrix[idy][idx] + matrix[idy][idx+1] < sum_matrix[idy][idx+1]:
                sum_matrix[idy][idx+1] = sum_matrix[idy][idx] + matrix[idy][idx+1]
                step_change = True

        return sum_matrix, step_change


def main():
    print(Day15AltAlt('input.txt').solve_1())
    print(Day15AltAlt('input_01.txt').solve_1())
    print(Day15AltAlt('input.txt').solve_2())
    print(Day15AltAlt('input_01.txt').solve_2())




if __name__ == '__main__':
    main()
