import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_unpacks_binary(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D2FE28
""")
    bitstream = puzzle.bitstream
    self.assertEqual(bitstream, [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0])

  def test_puzzle_pulls_literal_packets(self):
    puzzle = puz.Puzzle()
    puzzle.process("""D2FE28
""")
    packet = puzzle.get_packet()
    self.assertEqual(packet.version, 6)
    self.assertEqual(packet.id, 4)
    self.assertEqual(packet.literal, 2021)

  def test_puzzle_pulls_operator_packets_l0(self):
    puzzle = puz.Puzzle()
    puzzle.process("""38006F45291200
""")
    packet = puzzle.get_packet()
    self.assertEqual(packet.version, 1)
    self.assertEqual(packet.id, 6)
    self.assertEqual(packet.ltype, 0)
    self.assertEqual(packet.length, 27)
    sub1 = packet.subpackets[0]
    sub2 = packet.subpackets[1]
    self.assertEqual(sub1.literal, 10)
    self.assertEqual(sub2.literal, 20)

  def test_puzzle_pulls_operator_packets_l1(self):
    puzzle = puz.Puzzle()
    puzzle.process("""EE00D40C823060
""")
    packet = puzzle.get_packet()
    self.assertEqual(packet.version, 7)
    self.assertEqual(packet.id, 3)
    self.assertEqual(packet.ltype, 1)
    self.assertEqual(packet.length, 3)
    sub1 = packet.subpackets[0]
    sub2 = packet.subpackets[1]
    sub3 = packet.subpackets[2]
    self.assertEqual(sub1.literal, 1)
    self.assertEqual(sub2.literal, 2)
    self.assertEqual(sub3.literal, 3)

  def test_packet_evaluates_sum(self):
    packet = puz.Puzzle.Packet()
    packet.id = 0
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    self.assertEqual(packet.eval(), 123)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 123 + 345 + 345)

  def test_packet_evaluates_product(self):
    packet = puz.Puzzle.Packet()
    packet.id = 1
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    self.assertEqual(packet.eval(), 123)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 123 * 345 * 345)

  def test_packet_evaluates_min(self):
    packet = puz.Puzzle.Packet()
    packet.id = 2
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    self.assertEqual(packet.eval(), 123)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 123)

  def test_packet_evaluates_max(self):
    packet = puz.Puzzle.Packet()
    packet.id = 3
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    self.assertEqual(packet.eval(), 123)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 345)

  def test_packet_evaluates_gt(self):
    packet = puz.Puzzle.Packet()
    packet.id = 5
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 0)
    packet.subpackets = [s2, s1]
    self.assertEqual(packet.eval(), 1)

  def test_packet_evaluates_lt(self):
    packet = puz.Puzzle.Packet()
    packet.id = 6
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 1)
    packet.subpackets = [s2, s1]
    self.assertEqual(packet.eval(), 0)

  def test_packet_evaluates_eq(self):
    packet = puz.Puzzle.Packet()
    packet.id = 7
    s1 = puz.Puzzle.Packet()
    s1.id = 4
    s1.literal = 123
    packet.subpackets.append(s1)
    s2 = puz.Puzzle.Packet()
    s2.id = 4
    s2.literal = 345
    packet.subpackets.append(s2)
    self.assertEqual(packet.eval(), 0)
    packet.subpackets = [s2, s2]
    self.assertEqual(packet.eval(), 1)


if __name__ == '__main__':
    unittest.main()
