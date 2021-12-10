from dataclasses import dataclass


@dataclass
class LineParseObject:
    line: str
    is_incomplete: bool = False
    is_corrupted: bool = False
    illegal_character: str = ""
    would_complete: str = ""


class CorruptedChunkError(ValueError):
    pass


class IncompleteLineError(ValueError):
    pass


class Day10:
    closing_character_mapping = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">"
    }

    illegal_caracter_value = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    complete_character_value = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    def __init__(self, filename):
        with open(filename) as fd:
            self.lines = fd.readlines()

    def solve_1(self):
        corrupted_lines = []
        for line in self.lines:
            line = line.strip()
            parsed_chunk = self.verify_chunk(line)
            if parsed_chunk.is_corrupted:
                corrupted_lines.append([line, parsed_chunk.illegal_character])

        return sum([self.illegal_caracter_value[x[1]] for x in corrupted_lines])

    def solve_2(self):
        incomplete_lines = []
        for line in self.lines:
            line = line.strip()
            parsed_chunk = self.parse_line(line)
            if parsed_chunk.is_incomplete:
                incomplete_lines.append([line, parsed_chunk.would_complete])

        scores = []
        for line in incomplete_lines:
            sum = 0
            for char in line[1]:
                sum *= 5
                sum += self.complete_character_value[char]

            scores.append(sum)

        scores.sort()
        return scores[int((len(scores)-1)/2)]

    def parse_line(self, line):
        line = line.strip()
        while line:
            parsed_line = self.verify_chunk(line)
            if parsed_line.is_corrupted or parsed_line.is_incomplete:
                return parsed_line
            line = parsed_line.line

    def verify_chunk(self, line):
        if len(line) == 0:  # the line is finished
            return LineParseObject(line='', is_incomplete=True)

        if line[0] not in '([{<':  # the chunk is empty
            return LineParseObject(line=line)

        opening_character = line[0]
        expected_closing_character = self.closing_character_mapping[opening_character]
        parsed_line = self.verify_chunk(line[1:])
        if parsed_line.is_corrupted:
            return parsed_line
        if parsed_line.is_incomplete:
            parsed_line.would_complete = parsed_line.would_complete + expected_closing_character
            return parsed_line

        if len(parsed_line.line) == 0:  # incomplete line expecting a closing character
            return LineParseObject(line="", is_incomplete=True, would_complete=expected_closing_character)

        while parsed_line.line[0] in '([{<':
            parsed_line = self.verify_chunk(parsed_line.line)

            if parsed_line.is_corrupted:
                return parsed_line
            if parsed_line.is_incomplete:  # from recurssion well comes an incomplete parsed line. Adding the closing character we would expect
                parsed_line.would_complete = parsed_line.would_complete + expected_closing_character
                return parsed_line

            if len(parsed_line.line) == 0:  # incomplete line expecting a closing character
                return LineParseObject(line="", is_incomplete=True, would_complete=expected_closing_character)

        closing_character = parsed_line.line[0]
        if closing_character != self.closing_character_mapping[opening_character]:
            return LineParseObject(line=parsed_line.line, is_corrupted=True, illegal_character=closing_character)

        return LineParseObject(line=parsed_line.line[1:])


def main():
    print(Day10('input.txt').solve_1())
    print(Day10('input_01.txt').solve_1())
    print(Day10('input.txt').solve_2())
    print(Day10('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
