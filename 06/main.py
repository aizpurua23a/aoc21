from pprint import pprint


class Day6:
    def __init__(self, filename):
        with open(filename) as f:
            self.initial_nums = list(map(int, f.read().strip().split(',')))
        self.initial_day_puffers = {x: self.initial_nums.count(x) for x in range(9)}

    def handle_map_growth(self, day_puffer):
        mapping_function = {0: [1], 1: [2], 2: [3], 3: [4], 4: [5], 5: [6], 6: [0, 7], 7: [8], 8: [0]}
        return {new_value: sum(puffers if day in old_value_list else 0 for day, puffers in day_puffer.items())
                for new_value, old_value_list in mapping_function.items()}

    def solve(self, days):
        day_puffer_today = self.initial_day_puffers.copy()
        for day in range(1, days + 1):
            day_puffer_today = self.handle_map_growth(day_puffer_today)
        return sum(day_puffer_today.values())

    def solve_1(self):
        return self.solve(80)

    def solve_2(self):
        return self.solve(256)


if __name__ == '__main__':
    pprint(Day6('input_1.txt').solve_1())
    pprint(Day6('input_1.txt').solve_2())
