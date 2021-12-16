import numpy as np
from dataclasses import dataclass, field


@dataclass
class Packet:
    version: int
    type: int
    value: int = 0
    subpackets: list = field(default_factory=list)

    def __repr__(self):
        return f'v{self.version}-t{self.type}: {self.value}{self.subpackets}'


class Day16:
    def __init__(self, filename=None):
        if not filename:
            return
        with open(filename) as fd:
            self.input_packet = fd.read().strip()

    def solve_1(self):
        return self._get_version_sum_of_parsed_packet(self._parse_hex_packet(self.input_packet)[0])

    def solve_1_ex(self):
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('D2FE28')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('38006F45291200')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('EE00D40C823060')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('8A004A801A8002F478')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('620080001611562C8802118E34')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('C0015000016115A2E0802F182340')[0]))
        print(self._get_version_sum_of_parsed_packet(self._parse_hex_packet('A0016C880162017C3686B18A3D4780')[0]))

    def solve_2(self):
        return self._get_packet_value(self._parse_hex_packet(self.input_packet)[0])

    def solve_2_ex(self):
        print(self._get_packet_value(self._parse_hex_packet('C200B40A82')[0]))
        print(self._get_packet_value(self._parse_hex_packet('04005AC33890')[0]))
        print(self._get_packet_value(self._parse_hex_packet('880086C3E88112')[0]))
        print(self._get_packet_value(self._parse_hex_packet('CE00C43D881120')[0]))
        print(self._get_packet_value(self._parse_hex_packet('D8005AC2A8F0')[0]))
        print(self._get_packet_value(self._parse_hex_packet('F600BC2D8F')[0]))
        print(self._get_packet_value(self._parse_hex_packet('9C005AC2F8F0')[0]))
        print(self._get_packet_value(self._parse_hex_packet('9C0141080250320F1802104A08')[0]))

    def _parse_hex_packet(self, hex_packet):
        return self._parse_packet(self._get_binary_string(hex_packet))

    def _get_packet_value(self, parsed_packet):
        if parsed_packet.type == 0:
            return sum(self._get_packet_value(packet) for packet in parsed_packet.subpackets)

        if parsed_packet.type == 1:
            return np.prod([self._get_packet_value(packet) for packet in parsed_packet.subpackets])

        if parsed_packet.type == 2:
            return min(self._get_packet_value(packet) for packet in parsed_packet.subpackets)

        if parsed_packet.type == 3:
            return max(self._get_packet_value(packet) for packet in parsed_packet.subpackets)

        if parsed_packet.type == 4:
            return parsed_packet.value

        if parsed_packet.type == 5:
            return 1 if self._get_packet_value(parsed_packet.subpackets[0]) > self._get_packet_value(parsed_packet.subpackets[1]) else 0

        if parsed_packet.type == 6:
            return 1 if self._get_packet_value(parsed_packet.subpackets[0]) < self._get_packet_value(parsed_packet.subpackets[1]) else 0

        if parsed_packet.type == 7:
            return 1 if self._get_packet_value(parsed_packet.subpackets[0]) == self._get_packet_value(parsed_packet.subpackets[1]) else 0

    def _get_version_sum_of_parsed_packet(self, parsed_packet):
        version_sum = parsed_packet.version
        if parsed_packet.subpackets:
            for packet in parsed_packet.subpackets:
                version_sum += self._get_version_sum_of_parsed_packet(packet)

        return version_sum

    def _get_binary_string(self, hex_string):
        return ''.join(bin(int(char, 16))[2:].zfill(4) for char in hex_string)

    def _parse_packet(self, bin_stream):
        version = int(bin_stream[:3], 2)
        packet_type = int(bin_stream[3:6], 2)

        if packet_type == 4:
            result, remaining_stream, parsed_stream_length = self._parse_literal_value(bin_stream[6:])
        else:
            result, remaining_stream, parsed_stream_length = self._parse_operator_value(bin_stream[6:])

        parsed_stream_length += 6

        if isinstance(result, int):
            return Packet(version=version, type=packet_type, value=result), remaining_stream, parsed_stream_length
        else:
            return Packet(version=version, type=packet_type, subpackets=result), remaining_stream, parsed_stream_length

    def _parse_literal_value(self, stream):
        finished = False
        binary_string = ''
        parsed_stream_length = 0
        while not finished:
            finished = (stream[0] == '0')
            binary_string += stream[1:5]
            stream = stream[5:]
            parsed_stream_length += 5

        return int(binary_string, 2), stream, parsed_stream_length

    def _parse_operator_value(self, stream):
        length_type_id = int(stream[0])
        parsed_stream_length = 0

        if length_type_id == 0:
            subpackets_length = int(stream[1:16], 2)
            parsed_stream_length += 17
            stream = stream[16:]
            sub_packets = []
            while parsed_stream_length < subpackets_length + 17:
                packet, stream, sp_parsed_stream_length = self._parse_packet(stream)
                parsed_stream_length += sp_parsed_stream_length
                sub_packets.append(packet)

        else:
            subpackets_number = int(stream[1:12], 2)
            parsed_stream_length += 12
            stream = stream[12:]
            sub_packets = []
            for _ in range(subpackets_number):
                packet, stream, sp_parsed_stream_length = self._parse_packet(stream)
                parsed_stream_length += sp_parsed_stream_length
                sub_packets.append(packet)

        return sub_packets, stream, parsed_stream_length




def main():
    Day16().solve_1_ex()
    print(Day16('input_01.txt').solve_1())
    Day16().solve_2_ex()
    print(Day16('input_01.txt').solve_2())


if __name__ == '__main__':
    main()
