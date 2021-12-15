import sys
import numpy as np
class Graph: # Too Slow
    def __init__(self, nodes):
        self.nodes = nodes
        self.graph = None

        self.max_y, self.max_x = max(nodes)

    def _get_neighbor_coords(self, node):
        y = node[0]
        x = node[1]
        valid_coords = {}
        if x > 0:
            valid_coords[(y, x - 1)] = {}
        if x != self.max_x:
            valid_coords[(y, x + 1)] = {}
        if y > 0:
            valid_coords[(y - 1, x)] = {}
        if y != self.max_y:
            valid_coords[(y + 1, x)] = {}
        return valid_coords

    def construct_graph(self):
        graph = {(node[0], node[1]): self._get_neighbor_coords(node) for node in self.nodes}
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                graph[node][neighbor] = self.nodes[neighbor]

        self.graph = graph
        return graph


class Day15: # too slow
    def __init__(self, filename):
        with open(filename) as fd:
            matrix = []
            for row in fd.readlines():
                row = row.strip()
                matrix.append(list(map(int, row)))

        nodes = {}
        for idy, row in enumerate(matrix):
            for idx, value in enumerate(row):
                nodes[(idy, idx)] = value

        self.nodes = nodes
        self.graph = Graph(nodes).construct_graph()

    def solve_1(self):
        previous_nodes, shortest_path = self.dijkstra(self.graph)
        return shortest_path[max(self.nodes)]

    def dijkstra(self, graph):
        start_node = (0, 0)
        unvisited_nodes = list(graph)
        shortest_path = {}
        previous_nodes = {}
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value

        shortest_path[start_node] = 0

        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes:
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            neighbors = graph[current_min_node]
            for neighbor, move_cost in neighbors.items():

                tentative_value = shortest_path[current_min_node] + move_cost
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    previous_nodes[neighbor] = current_min_node

            unvisited_nodes.remove(current_min_node)
        return previous_nodes, shortest_path

    def print_result(self, previous_nodes, shortest_path, start_node, target_node):
        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # Add the start node manually
        path.append(start_node)

        print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
        print(" -> ".join(reversed(path)))


class Day15Alt: # Not working
    def __init__(self, filename):
        with open(filename) as fd:
            matrix = []
            for row in fd.readlines():
                row = row.strip()
                matrix.append(list(map(int, row)))
        self.matrix = matrix

    def solve_1(self):
        stationary_path = self.find_stationary_path(self.matrix)

    def find_stationary_path(self, matrix):
        start = (0, 0)
        end = (9, 9)

        max_y = end[0]
        max_x = end[1]

        starting_path = self.get_initial_path(end)
        starting_cost = self.get_path_cost(starting_path, matrix)
        changed = True
        path = starting_path
        while changed:
            changed = False
            for idp, point in enumerate(path):
                # * * -> * .
                # . * -> * *
                y, x = point
                if x == max_x or y == max_y:
                    continue

                if path[idp+1] == (y, x+1) and matrix[y+1][x] < matrix[y][x+1]:
                    path[idp+1] = (y+1, x)
                    changed = True
                    break

                if path[idp+1] == (y+1, x) and matrix[y][x+1] < matrix[y+1][x]:
                    path[idp+1] = (y, x+1)
                    changed = True
                    break

        return path






    def get_path_cost(self, path, matrix):
        return sum(value for idy, row in enumerate(matrix) for idx, value in enumerate(row) if (idy, idx) in path)

    def get_initial_path(self, end):
        initial_path = []
        initial_path.append((0, 0))
        for i in range(1, end[0]+1):
            initial_path.append((i-1, i))
            initial_path.append((i, i))

        return initial_path


class Day15AltAlt:
    def __init__(self, filename):
        with open(filename) as fd:
            matrix = []
            for row in fd.readlines():
                row = row.strip()
                matrix.append(list(map(int, row)))
        self.matrix = np.array(matrix)

    def solve_2(self):
        row_matrices = []
        for col_step in range(5):
            row = []
            for row_step in range(5):
                row.append(self.get_updated_matrix(self.matrix, col_step + row_step))
            row_matrix = np.concatenate(row, axis=1)
            row_matrices.append(row_matrix)
        big_matrix = np.concatenate(row_matrices, axis=0)

        sum_matrix = self.get_optimal_sum_matrix(big_matrix)
        return sum_matrix[-1][-1]




    def get_updated_matrix(self, matrix, step):
        return np.vectorize(lambda x: (x-1+step) % 9+1)(matrix)

    def solve_1(self):
        sum_matrix = self.get_optimal_sum_matrix(self.matrix)
        return sum_matrix[-1][-1]

    def get_optimal_sum_matrix(self, matrix):
        max_y = np.size(matrix, 0)
        max_x = np.size(matrix, 1)

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

        changed = True
        while changed:
            changed = False
            for idy in range(max_y):
                for idx in range(max_x):
                    sum_matrix, step_change = self.update_sum_matrix(idy, idx, matrix, sum_matrix)
                    if step_change:
                        changed = True

        return sum_matrix

    def update_sum_matrix(self, idy, idx, matrix, sum_matrix):
        max_y = np.size(self.matrix, 0)
        max_x = np.size(self.matrix, 1)
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
    #print(Day15AltAlt('input.txt').solve_1())
    #print(Day15AltAlt('input_01.txt').solve_1())
    print(Day15AltAlt('input.txt').solve_2())
    print(Day15AltAlt('input_01.txt').solve_2())




if __name__ == '__main__':
    main()
