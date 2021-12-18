from math import floor, ceil
from functools import reduce

class Day18:
    def __init__(self, filename=None):
        if not filename:
            return

        with open(filename) as fd:
            self.snailnum_list = fd.read().strip().split('\n')

    def solve_2(self):
        return max([self._get_magnitude(self._add_snailnum_list([y, x]))
                    for idx, x in enumerate(self.snailnum_list)
                    for idy, y in enumerate(self.snailnum_list)
                    if idx != idy])

    def solve_1(self):
        return self._get_magnitude(self._add_snailnum_list(self.snailnum_list))

    def solve_eg_1(self):
        pass

    # self._explode_once([[[[[9, 8], 1], 2], 3], 4])
    # self._explode_once([7, [6, [5, [4, [3, 2]]]]])
    # self._explode_once([[6, [5, [4, [3, 2]]]], 1])
    # self._explode_once([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    # self._explode_once([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    # self._split_once([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
    # self._split_once([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])

    # print(self._add_snailnums([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]))
    # print(self._add_snailnum_list("[1,1]\n[2,2]\n[3,3]\n[4,4]\n"))
    # print(self._add_snailnum_list("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n"))
    # print(self._add_snailnum_list("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]\n"))
    # print(self._add_snailnum_list(
    #    "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]\n[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]\n[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]\n[7,[5,[[3,8],[1,4]]]]\n[[2,[2,2]],[8,[8,1]]]\n[2,9]\n[1,[[[9,3],9],[[9,0],[0,7]]]]\n[[[5,[7,4]],7],1]\n[[[[4,2],2],6],[8,7]]\n"))

    # print(self._get_magnitude([9, 1]))
    # print(self._get_magnitude([1, 9]))
    # print(self._get_magnitude([[9, 1], [1, 9]]))
    # print(self._get_magnitude([[1, 2], [[3, 4], 5]]))
    # print(self._get_magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]))
    # print(self._get_magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]))
    # print(self._get_magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]))
    # print(self._get_magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]))
    # print(self._get_magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]))

    def _get_magnitude(self, snailnum):
        return self._get_magnitude(snailnum[0]) * 3 + self._get_magnitude(snailnum[1]) * 2 if isinstance(snailnum, list) else snailnum

    def _add_snailnum_list(self, snailnum_string_list):
        snailnum_list = [list(eval(snailnum)) for snailnum in snailnum_string_list]
        return reduce(self._add_snailnums, snailnum_list)

    def _add_snailnums(self, left, right):
        snailnum = [left, right]
        while True:
            snailnum, exlpoded = self._explode_once(snailnum)
            if exlpoded:
                continue
            snailnum, split = self._split_once(snailnum)
            if split:
                continue
            break
        return snailnum

    def _explode_once(self, num_pair):
        result = self._explode_first_match(num_pair, 0)
        return result[0], result[3]

    def _split_once(self, snailnum):
        return self._split_first_match(snailnum)

    def _can_be_exploded(self, num_pair, depth):
        if depth >= 4 and isinstance(num_pair, list):
            return True

        return self._can_be_exploded(num_pair[0], depth + 1) if isinstance(num_pair[0], list) else False or \
            self._can_be_exploded(num_pair[1], depth + 1) if isinstance(num_pair[1], list) else False

    def _explode_first_match(self, num_pair, depth, first_match_exploded=False):
        if isinstance(num_pair, int):
            return num_pair, None, None, first_match_exploded

        if depth >= 4 and isinstance(num_pair, list) and isinstance(num_pair[0], int) and isinstance(num_pair[1], int):
            return 0, num_pair[0], num_pair[1], True

        left_items, left, right, first_match_exploded = self._explode_first_match(num_pair[0], depth + 1,
                                                                                  first_match_exploded)
        if right is not None:
            return [left_items, self._add_from_left(right, num_pair[1])], left, None, first_match_exploded

        right_items = num_pair[1]
        if not first_match_exploded:
            right_items, left, right, first_match_exploded = self._explode_first_match(num_pair[1], depth + 1,
                                                                                       first_match_exploded)
            if left is not None:
                return [self._add_from_right(left, num_pair[0]), right_items], None, right, first_match_exploded

        return [left_items, right_items], left, right, first_match_exploded

    def _add_from_left(self, value, num_pair):
        return [self._add_from_left(value, num_pair[0]), num_pair[1]] if isinstance(num_pair, list) \
            else num_pair + value

    def _add_from_right(self, value, num_pair):
            return [num_pair[0], self._add_from_right(value, num_pair[1])] if isinstance(num_pair, list) \
                else num_pair + value

    def _split_first_match(self, snailnum, first_match_split=False):
        if first_match_split:
            return snailnum, first_match_split

        if isinstance(snailnum, int) and snailnum > 9:
            return [floor(snailnum / 2), ceil(snailnum / 2)], True

        if isinstance(snailnum, int):
            return snailnum, first_match_split

        left_side, first_match_split = self._split_first_match(snailnum[0])
        right_side = snailnum[1]
        if not first_match_split:
            right_side, first_match_split = self._split_first_match(snailnum[1])
        return [left_side, right_side], first_match_split


def main():
    Day18().solve_eg_1()
    print(Day18('input.txt').solve_1())
    print(Day18('input_01.txt').solve_1())

    print(Day18('input.txt').solve_2())
    print(Day18('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
