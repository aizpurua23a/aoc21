import numpy as np


class Day13:
    def __init__(self, filename):
        dots = []
        folds = []

        with open(filename) as fd:
            dot_positions, fold_positions = fd.read().split('\n\n')

        for dot in dot_positions.splitlines():
            dots.append(list(map(int, [coord for coord in dot.strip().split(',')])))

        for fold in fold_positions.splitlines():
            coord, num = fold.strip().split("fold along ")[1].split('=')
            folds.append([coord, int(num)])

        max_x = max([a[0] for a in dots]) + 1
        max_y = max([a[1] for a in dots]) + 1

        self.paper = np.zeros((max_y, max_x), dtype=int)
        self.folds = folds

        for dot in dots:
            self.paper[dot[1]][dot[0]] = 1

    def solve_1(self):
        new_paper = self.fold_paper(self.paper, self.folds[0])
        return np.sum(new_paper)

    def solve_2(self):
        paper = self.paper
        for fold in self.folds:
            paper = self.fold_paper(paper, fold)
        self.print_paper(paper)

    def fold_paper(self, old_paper, fold):
        if fold[0] == 'x':
            paper = self.fold_along_the_x_axis(old_paper, fold[1])
        else:
            paper = self.fold_along_the_y_axis(old_paper, fold[1])
        return paper

    def fold_along_the_y_axis(self, paper, fold_line):
        if fold_line != (len(paper)-1)/2:
            print('Something is wrong')
        new_paper = np.zeros((fold_line, len(paper[0])), dtype=int)
        for idy in range(0, fold_line):
            for idx in range(0, len(paper[0])):
                new_paper[idy][idx] = paper[idy][idx] or paper[-idy-1][idx]
        return new_paper

    def fold_along_the_x_axis(self, paper, fold_line):
        if fold_line != (len(paper[0])-1)/2:
            print('Something is wrong')
        new_paper = np.zeros((len(paper), fold_line), dtype=int)
        for idy in range(0,  len(paper)):
            for idx in range(0, fold_line):
                new_paper[idy][idx] = paper[idy][idx] or paper[idy][-idx-1]
        return new_paper

    def print_paper(self, paper):
        for row in paper:
            print_row = ''
            for item in row:
                print_row += '.' if item == 0 else '#'

            print(print_row)


def main():
    print(Day13('input.txt').solve_1())
    print(Day13('input_01.txt').solve_1())

    Day13('input.txt').solve_2()
    Day13('input_01.txt').solve_2()


if __name__ == '__main__':
    main()
