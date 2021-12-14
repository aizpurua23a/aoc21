class Node:
    def __init__(self, name, all_known_edges):
        self.name = name
        self.neighbors = []
        for edge in all_known_edges:
            if self.name in edge:
                self.neighbors.append(edge[0] if edge[1] == self.name else edge[1])

    def __repr__(self):
        return f'{self.name} - neighbors: {self.neighbors}'


class Day12:
    def __init__(self, filename):
        edges = []
        with open(filename) as fd:
            for line in fd.readlines():
                edges.append(tuple(line.strip().split('-')))

        node_names_set = set([item for sublist in edges for item in sublist])
        self.nodes = [Node(node, edges) for node in node_names_set]

    def solve_1(self):
        self.solve()

    def solve_2(self):
        self.solve(True)

    def solve(self, one_repeated=False):
        paths = [[self.get_node_of_name('start').name]]
        while not all(path[-1] == 'end' for path in paths):
            new_path_list = []
            for path in paths:
                if path[-1] == 'end':
                    new_path_list.append(path)
                    continue

                last_node = self.get_node_of_name(path[-1])
                new_paths = [path + [neighbor] for neighbor in last_node.neighbors
                             if self.has_no_repeated_small_cave(path + [neighbor], one_repeated=one_repeated)]

                [new_path_list.append(path) for path in new_paths]

            paths = new_path_list
        return len(paths)

    def has_no_repeated_small_cave(self, path, one_repeated=False):
        small_caves = set()
        one_repeated_cave = False
        for node_name in path:
            if node_name.islower() and node_name in small_caves:
                if one_repeated and not one_repeated_cave and node_name not in ('start', 'end'):
                    one_repeated_cave = True
                    continue
                return False
            if node_name.islower():
                small_caves.add(node_name)
        return True

    def get_node_of_name(self, name):
        return [node for node in self.nodes if node.name == name][0] or None


def main():
    print(Day12('input_eg_0.txt').solve_1())
    print(Day12('input_eg_1.txt').solve_1())
    print(Day12('input_eg_2.txt').solve_1())
    print(Day12('input_01.txt').solve_1())

    print(Day12('input_eg_0.txt').solve_2())
    print(Day12('input_eg_1.txt').solve_2())
    print(Day12('input_eg_2.txt').solve_2())
    print(Day12('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
