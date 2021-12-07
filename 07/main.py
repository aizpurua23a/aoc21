import statistics
from pprint import pprint


class Day7:
    def __init__(self, filename):
        with open(filename) as fd:
            self.positions = list(map(int, fd.read().strip().split(',')))

        self.calculated_fuel_consumptions = {}
        self.calculated_fuel_consumptions_triangle = {}

    def solve_1(self):
        return self.solve()

    def solve_2(self):
        return self.solve(trig=True)

    def solve(self, trig=False):
        guess = round(statistics.mean(self.positions))
        done = False
        guess_fuel = None
        while not done:
            guess_fuel = self.get_fuel_consumption(guess, trig)
            next_fuel = self.get_fuel_consumption(guess + 1, trig)
            previous_fuel = self.get_fuel_consumption(guess - 1, trig)
            done = bool(guess_fuel < next_fuel and guess_fuel < previous_fuel)
            if not done:
                if next_fuel < guess_fuel:
                    guess = guess + 1
                elif previous_fuel < guess_fuel:
                    guess = guess - 1
                else:
                    raise ValueError("Something went wrong")
        return guess, guess_fuel

    def get_fuel_consumption(self, guess, trig=False):
        if trig:
            return self.get_fuel_consumption_to_pos_triangle(guess)
        return self.get_fuel_consumption_to_pos(guess)

    def get_fuel_consumption_to_pos(self, guess):
        if guess in self.calculated_fuel_consumptions.keys():
            return self.calculated_fuel_consumptions[guess]

        guess_fuel = sum([abs(guess - x) for x in self.positions])
        self.calculated_fuel_consumptions[guess] = guess_fuel
        return guess_fuel

    def get_fuel_consumption_to_pos_triangle(self, guess):
        if guess in self.calculated_fuel_consumptions_triangle.keys():
            return self.calculated_fuel_consumptions_triangle[guess]
        fuel = sum([int((abs(guess - x) * (abs(guess - x) + 1))/2) for x in self.positions])
        self.calculated_fuel_consumptions_triangle[guess] = fuel
        return fuel


def main():
    pprint(Day7('input.txt').solve_1())
    pprint(Day7('input_01.txt').solve_1())
    pprint(Day7('input.txt').solve_2())
    pprint(Day7('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
