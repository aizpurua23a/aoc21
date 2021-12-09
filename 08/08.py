class Day8:
    def __init__(self, filename):
        with open(filename) as fd:
            self.input_list = []
            for line in fd.readlines():
                line = line.strip()
                left_side, right_side = line.split(' | ')
                self.input_list.append([left_side.split(' '), right_side.split(' ')])

    def solve_1(self):
        return sum(1 if len(digit) in (2, 3, 4, 7) else 0 for _, right_side_digits in self.input_list for digit in right_side_digits)

    def solve_2(self):
        outputs = []
        for left_side_digits, right_side_digits in self.input_list:
            mapping = self.get_mapping_from_left_side_digits(left_side_digits)
            output = [mapping.index(set(digit)) for digit in right_side_digits]
            outputs.append(sum(element * 10 ** (3 - idx) for idx, element in enumerate(output)))
        return sum(outputs)

    def get_mapping_from_left_side_digits(self, left_side_digits):
        one, four, seven, eight = self.get_unique_len_nums(left_side_digits)
        zero, six, nine = self.get_six_segment_nums(left_side_digits, one, four)
        two, three, five = self.get_five_segment_nums(left_side_digits, one, nine)
        return list(map(set, [zero, one, two, three, four, five, six, seven, eight, nine]))

    def get_unique_len_nums(self, digit_list):
        return (
            [x for x in digit_list if len(x) == 2][0],
            [x for x in digit_list if len(x) == 4][0],
            [x for x in digit_list if len(x) == 3][0],
            [x for x in digit_list if len(x) == 7][0]
        )

    def get_six_segment_nums(self, digit_list, one, four):
        six_item_digits = [x for x in digit_list if len(x) == 6]
        # SIX is the six-item digit that is missing one segment that is present in ONE:
        six = [digit for digit in six_item_digits if any(character not in digit for character in one)][0]
        six_item_digits.remove(six)
        # ZERO is the remaining six-item digit that is missing one segment present in FOUR
        zero = [digit for digit in six_item_digits if any(character not in digit for character in four)][0]
        six_item_digits.remove(zero)
        # the remaining element must be NINE
        nine = six_item_digits[0]

        return zero, six, nine

    def get_five_segment_nums(self, digit_list, one, nine):
        five_item_digits = [x for x in digit_list if len(x) == 5]

        # THREE is the only five-segment digit that fully includes ONE
        three = [digit for digit in five_item_digits if all(character in digit for character in one)][0]
        five_item_digits.remove(three)

        # FIVE is fully included in NINE -> non-NINE segment implies TWO
        two = [digit for digit in five_item_digits if any(character not in nine for character in digit)][0]
        five_item_digits.remove(two)

        # remaining five-segment number must be FIVE
        five = five_item_digits[0]
        return two, three, five


def main():
    print(Day8('input.txt').solve_1())
    print(Day8('input_01.txt').solve_1())
    print(Day8('input.txt').solve_2())
    print(Day8('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
