from pprint import pprint
from itertools import chain


class Board:
    def __init__(self):
        self.rows = []
        self.hits_per_row = [0] * 5
        self.hits_per_col = [0] * 5

    def add_row(self, new_row):
        self.rows.append(new_row)

    def update_hits_and_return_wins(self, new_num):
        for idx, row in enumerate(self.rows):
            self.hits_per_row[idx] += 1 if new_num in row else 0
        for idx in range(5):
            self.hits_per_col[idx] += 1 if any(new_num == row[idx] for row in self.rows) else 0
        return 5 in self.hits_per_row or 5 in self.hits_per_col

    def get_sum_of_unmarked_numbers(self, called_nums):
        return sum(set(chain(*self.rows)).difference(set(called_nums)))


class Day4:
    def __init__(self, filename):
        self.bingo_nums = []
        self.boards = []

        with open(filename) as file:
            self.bingo_nums = map(int, file.readline().strip().split(','))
            self.boards = []
            for line in file.readlines():
                if line == '\n':
                    self.boards.append(Board())
                    continue
                nums = map(int, line.strip().replace('  ', ' ').replace(' ', ',').split(','))
                self.boards[-1].add_row(list(nums))

    def solve_1(self):
        called_nums = []
        for id_num, num in enumerate(self.bingo_nums):
            called_nums.append(num)
            print(f'Number {num}')
            for idx, board in enumerate(self.boards):
                if board.update_hits_and_return_wins(num):
                    sum_of_unmarked_nums = board.get_sum_of_unmarked_numbers(called_nums)
                    pprint(f'Board {idx} wins!')
                    pprint(f'Sum is {sum_of_unmarked_nums}, num is {num}, result is {sum_of_unmarked_nums * num}')
                    return

    def solve_2(self):
        called_nums = []
        next_boards = self.boards
        for id_num, num in enumerate(self.bingo_nums):
            called_nums.append(num)
            current_boards = next_boards
            next_boards = current_boards.copy()

            for idx, board in enumerate(current_boards):
                if not board.update_hits_and_return_wins(num):
                    continue

                if len(current_boards) == 1:
                    sum_of_unmarked_nums = board.get_sum_of_unmarked_numbers(called_nums)
                    pprint(f'Sum is {sum_of_unmarked_nums}, num is {num}, result is {sum_of_unmarked_nums * num}')
                    return

                next_boards.remove(board)


if __name__ == '__main__':
    #Day4('input.txt').solve_1()
    #Day4('input_01.txt').solve_1()
    #Day4('input.txt').solve_2()
    Day4('input_01.txt').solve_2()
