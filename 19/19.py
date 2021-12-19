import numpy as np
from pprint import pprint


def _3d_rotations():
    matrix = np.eye(3, dtype=int)

    x_rotation = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    y_rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    y_minus_rotation = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    z_rotation = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

    for _ in range(4):
        for _ in range(4):
            yield matrix
            matrix = np.matmul(x_rotation, matrix)
        matrix = np.matmul(z_rotation, matrix)
    matrix = np.matmul(y_rotation, matrix)
    for _ in range(4):
        yield matrix
        matrix = np.matmul(x_rotation, matrix)
    matrix = np.matmul(y_minus_rotation, np.eye(3, dtype=int))
    for _ in range(4):
        yield matrix
        matrix = np.matmul(x_rotation, matrix)


def _2d_rotations():
    matrix = np.eye(2, dtype=int)
    z_rotation = np.array([[0, 1], [-1, 0]])
    for _ in range(4):
        yield matrix
        matrix = np.matmul(z_rotation, matrix)


class Day19:
    def __init__(self, filename=None):
        if not filename:
            return

        with open(filename) as fd:
            scanner_strs = fd.read().split('\n\n')
            self.scanner_beacons = []
            for scanner_str in scanner_strs:
                lines = scanner_str.strip().split('\n')
                detected_beacons_rel_coords = []
                for line in lines[1:]:
                    detected_beacons_rel_coords.append(np.array(list(map(int, line.strip().split(',')))))

                self.scanner_beacons.append(detected_beacons_rel_coords)

    def solve_1_2d_ex(self):
        absolute_beacons = []
        for relative_beacon_position in self.scanner_beacons[0]:
            absolute_beacons.append(relative_beacon_position)

        scanners_offset_and_rotation = [[0, 0], np.eye(2, dtype=int).tolist()]
        for scanner in self.scanner_beacons[1:]:

            for scanner_rotation_candidate in _2d_rotations():
                new_beacons_rotated_relative_position = self._rotate(scanner_rotation_candidate, scanner)
                # to be expanded to a new loop, the first beacon need not be in the already existing beacon set
                first_rotated_beacon_coords = new_beacons_rotated_relative_position[0]

                for absolute_beacon_pos in absolute_beacons:
                    scanner_offset_candidate = absolute_beacon_pos - first_rotated_beacon_coords
                    new_beacons_absolute_position_candidate = list(new_beacons_rotated_relative_position + scanner_offset_candidate)
                    hits = len(list(filter(lambda x: x.tolist() in [b.tolist() for b in absolute_beacons], new_beacons_absolute_position_candidate)))

                    if hits == len(absolute_beacons):
                        scanners_offset_and_rotation.append([scanner_offset_candidate.tolist(), scanner_rotation_candidate.tolist()])

        return scanners_offset_and_rotation

    def solve_1_3d_ex(self):
        absolute_beacons = []
        for relative_beacon_position in self.scanner_beacons[0]:
            absolute_beacons.append(relative_beacon_position)

        scanners_offset_and_rotation = [[0, 0, 0], np.eye(3, dtype=int).tolist()]
        for scanner in self.scanner_beacons[1:]:

            for scanner_rotation_candidate in _3d_rotations():
                new_beacons_rotated_relative_position = self._rotate(scanner_rotation_candidate, scanner)
                # to be expanded to a new loop, the first beacon need not be in the already existing beacon set
                first_rotated_beacon_coords = new_beacons_rotated_relative_position[0]

                for absolute_beacon_pos in absolute_beacons:
                    scanner_offset_candidate = absolute_beacon_pos - first_rotated_beacon_coords
                    new_beacons_absolute_position_candidate = list(
                        new_beacons_rotated_relative_position + scanner_offset_candidate)
                    hits = len(list(filter(lambda x: x.tolist() in [b.tolist() for b in absolute_beacons],
                                           new_beacons_absolute_position_candidate)))

                    if hits == len(absolute_beacons):
                        scanners_offset_and_rotation.append(
                            [scanner_offset_candidate.tolist(), scanner_rotation_candidate.tolist()])

        return scanners_offset_and_rotation

    def _rotate(self, rotation, scanner):
        return [np.matmul(rotation, beacon) for beacon in scanner]

    def solve_1_3d(self):
        absolute_beacons = []
        for relative_beacon_position in self.scanner_beacons[0]:
            absolute_beacons.append(relative_beacon_position.tolist())

        scanners_offset_and_rotation = [None] * len(self.scanner_beacons)
        scanners_offset_and_rotation[0] = [[0, 0, 0], np.eye(3, dtype=int).tolist()]

        done = False
        remaining_scanners = [{'id': idx+1, 'beacons': beacons} for idx, beacons in enumerate(self.scanner_beacons[1:])]
        while not done:
            for scanner_data in remaining_scanners:
                hit = False
                beacons = scanner_data.get('beacons')
                for scanner_rotation_candidate in _3d_rotations():
                    new_beacons_rotated_relative_position = self._rotate(scanner_rotation_candidate, beacons)
                    for pivot_beacon in new_beacons_rotated_relative_position:
                        for absolute_beacon_pos in absolute_beacons:
                            scanner_offset_candidate = absolute_beacon_pos - pivot_beacon
                            new_beacons_absolute_position_candidate = (new_beacons_rotated_relative_position + scanner_offset_candidate).tolist()
                            hits = len([x for x in new_beacons_absolute_position_candidate if x in absolute_beacons])
                            if hits >= 12:
                                scanners_offset_and_rotation[scanner_data.get('id')] \
                                    = [scanner_offset_candidate.tolist(), scanner_rotation_candidate.tolist()]
                                absolute_beacons = self._add_new_beacons(absolute_beacons, new_beacons_absolute_position_candidate)
                                print(f'Found scanner {scanner_data.get("id")} in position {scanner_offset_candidate}')
                                remaining_scanners.remove(scanner_data)
                                hit = True
                                break
                        if hit:
                            break
                    if hit:
                        break
                if hit:
                    break
            if not remaining_scanners:
                break
        return len(absolute_beacons)

    def _add_new_beacons(self, absolute_beacons, new_scanner_beacons):
        new_beacons = [beacon for beacon in new_scanner_beacons if beacon not in [b for b in absolute_beacons]]
        return absolute_beacons + new_beacons

    def solve_2(self, filename):
        with open(filename) as fd:
            lines = fd.readlines()
        scanners = [list(map(int, [value for value in line.strip().split(',')])) for line in lines]
        distances = [sum(abs(s1[i] - s2[i]) for i in range(3))
                     for idx, s2 in enumerate(scanners) for idy, s1 in enumerate(scanners)]
        return np.max(distances)


def main():
    #Day19('input_2d_ex.txt').solve_1_2d_ex()
    #Day19('input_3d_ex.txt').solve_1_3d_ex()
    #print(Day19('input_3d_ex_2.txt').solve_1_3d())
    #print(Day19('input_01.txt').solve_1_3d())
    print(Day19().solve_2('positions.txt'))


if __name__ == '__main__':
    main()
