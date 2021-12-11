import numpy as np


class Day11:
    def __init__(self, filename):
        self.starting_energy = []
        self.total_flashes = 0
        with open(filename) as fd:
            for line in fd.readlines():
                self.starting_energy.append(list(map(int, (char for char in line.strip()))))
            self.starting_energy = np.array(self.starting_energy, dtype=int)

    def solve_1(self):
        return self.simulate_days(100)

    def solve_2(self):
        return self.simulate_until_first_sync_flash()

    def simulate_until_first_sync_flash(self):
        starting_day_energy = self.starting_energy.copy()
        sync_flash = False
        step = 0
        while not sync_flash:
            step += 1
            starting_flashes = self.total_flashes

            unflashed_energy = starting_day_energy + np.ones(shape=(len(starting_day_energy), len(starting_day_energy)))
            starting_day_energy = self.calculate_flashed_energy(unflashed_energy)

            flash_delta = self.total_flashes - starting_flashes
            if flash_delta == len(unflashed_energy) ** 2:
                return step

        return self.total_flashes

    def simulate_days(self, total_days):
        starting_day_energy = self.starting_energy.copy()
        for day in range(total_days):
            unflashed_energy = starting_day_energy + np.ones(shape=(len(starting_day_energy), len(starting_day_energy)))
            starting_day_energy = self.calculate_flashed_energy(unflashed_energy)

        return self.total_flashes

    def calculate_flashed_energy(self, unflashed_energy):
        energy_array = unflashed_energy.copy()

        any_flashed = True
        while any_flashed:
            any_flashed = False

            for idy, row in enumerate(energy_array):
                for idx, energy_level in enumerate(row):
                    if energy_level <= 9:
                        continue
                    energy_array = self.update_new_energy_array_after_this_flash(energy_array, idy, idx)
                    any_flashed = True
                    self.total_flashes += 1

        return energy_array

    def update_new_energy_array_after_this_flash(self, new_energy_array, idy, idx):
        if new_energy_array[idy][idx] <= 9:
            raise ValueError("Something went wrong. This value already flashed")
        new_energy_array[idy][idx] = 0
        for delta_y in [-1, 0, 1]:
            for delta_x in [-1, 0, 1]:
                if idy + delta_y < 0 or idy + delta_y >= len(new_energy_array):
                    continue
                if idx + delta_x < 0 or idx + delta_x >= len(new_energy_array):
                    continue
                if new_energy_array[idy + delta_y][idx + delta_x] == 0:
                    continue

                new_energy_array[idy + delta_y][idx + delta_x] += 1
        return new_energy_array


def main():
    print(Day11('input.txt').solve_1())
    print(Day11('input_01.txt').solve_1())
    print(Day11('input.txt').solve_2())
    print(Day11('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
