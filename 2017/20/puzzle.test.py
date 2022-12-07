import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_particles(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

    p1 = puzzle.particles[0]
    p2 = puzzle.particles[1]

    self.assertEquals(p1.p, (3, 0, 0))
    self.assertEquals(p2.v, (0, 0, 0))
    self.assertEquals(p2.a, (-2, 0, 0))

  def test_puzzle_particles_simulate(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

    p1 = puzzle.particles[0]
    p2 = puzzle.particles[1]

    p1.simulate()
    p2.simulate()

    self.assertEquals(p1.p, (4, 0, 0))
    self.assertEquals(p2.v, (-2, 0, 0))
    self.assertEquals(p2.a, (-2, 0, 0))

  def test_puzzle_particles_know_last_and_current_distance(self):
    puzzle = puz.Puzzle()
    puzzle.process("""p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""")

    p1 = puzzle.particles[0]
    p2 = puzzle.particles[1]

    p1.simulate()
    p2.simulate()

    self.assertEquals(p1.last_distance, 3)
    self.assertEquals(p2.last_distance, 4)

    self.assertEquals(p1.current_distance, 4)
    self.assertEquals(p2.current_distance, 2)

if __name__ == '__main__':
    unittest.main()
