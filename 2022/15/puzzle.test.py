import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_maps_sensors(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sensor at x=2, y=18: closest beacon is at x=-20, y=23
Sensor at x=14, y=23: closest beacon is at x=12, y=-2
""")
    sensors = puzzle.sensors

    self.assertEquals(sensors[0], ((2,18), (-20, 23)))
    self.assertEquals(sensors[1], ((14,23), (12, -2)))

  def test_does_not_have_beacon_within_range_of_closest(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sensor at x=2, y=18: closest beacon is at x=-20, y=23
Sensor at x=14, y=23: closest beacon is at x=12, y=-2
""")

    self.assertEquals(puzzle.is_beacon(1,19), False)

  def test_does_have_beacon_within_at_known(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sensor at x=2, y=18: closest beacon is at x=-20, y=23
Sensor at x=14, y=23: closest beacon is at x=12, y=-2
""")

    self.assertEquals(puzzle.is_beacon(-20,23), True)
    
  def test_does_not_know_beacon_outside_all_sensor_ranges(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sensor at x=2, y=18: closest beacon is at x=-20, y=23
Sensor at x=14, y=23: closest beacon is at x=12, y=-2
""")

    self.assertEquals(puzzle.is_beacon(-26,18), None)

  def test_calculates_edge_outside_range(self):
    puzzle = puz.Puzzle()
    puzzle.process("""Sensor at x=2, y=18: closest beacon is at x=-20, y=23
Sensor at x=14, y=23: closest beacon is at x=12, y=-2
""")

    beacon = ((0,0), (0,1))
    perim = puzzle.calc_edge(beacon)

    self.assertEquals((-2, 0) in perim, True)
    self.assertEquals(( 2, 0) in perim, True)
    self.assertEquals((-1,-1) in perim, True)
    self.assertEquals(( 1,-1) in perim, True)
    self.assertEquals((-1, 1) in perim, True)
    self.assertEquals(( 1, 1) in perim, True)
    self.assertEquals(( 0,-2) in perim, True)
    self.assertEquals(( 0, 2) in perim, True)
    self.assertEquals(len(perim), 8)

if __name__ == '__main__':
    unittest.main()
