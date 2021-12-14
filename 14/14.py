class Day14:
    def __init__(self, filename):
        with open(filename) as fd:
            chain, rules = fd.read().split('\n\n')
        rule_list = list(map(lambda x: x.split(' -> '), rules.strip().split('\n')))
        rule_map = {rule[0]: rule[1] for rule in rule_list}

        self.pairs = {item: 0 for item in rule_map}
        for idx in range(len(chain)-1):
            self.pairs[f'{chain[idx]}{chain[idx+1]}'] += 1

        pair_rule_map = {key: [key[0] + value, value + key[1]] for key, value in rule_map.items()}
        self.reversed_pair_map = {pair: [from_pair for from_pair, to_pair in pair_rule_map.items() if pair in to_pair]
                                  for pair in self.pairs}

        self.edges = [chain[0], chain[-1]]

    def solve_1(self):
        pairs = self.pairs
        for _ in range(10):
            pairs = self._update_pairs_with_rules(pairs)
        count_map = self._get_count_map_from_pairs(pairs)
        return max(count_map.values()) - min(count_map.values())

    def solve_2(self):
        pairs = self.pairs
        for _ in range(40):
            pairs = self._update_pairs_with_rules(pairs)
        count_map = self._get_count_map_from_pairs(pairs)
        return max(count_map.values()) - min(count_map.values())

    def _update_pairs_with_rules(self, pairs):
        new_pairs = {}
        for pair in pairs:
            originating_pairs = self.reversed_pair_map[pair]
            new_pairs[pair] = sum(pairs[originating_pair] for originating_pair in originating_pairs)

        return new_pairs

    def _get_count_map_from_pairs(self, pairs):
        characters = set(''.join(pairs))
        count_map = {}
        for char in characters:
            count_map[char] = sum(value * key.count(char) for key, value in pairs.items() if char in key)

        count_map[self.edges[0]] += 1
        count_map[self.edges[1]] += 1
        count_map = {key: int(value/2) for key, value in count_map.items()}
        return count_map

def main():
    print(Day14('input.txt').solve_1())
    print(Day14('input_01.txt').solve_1())
    print(Day14('input.txt').solve_2())
    print(Day14('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
