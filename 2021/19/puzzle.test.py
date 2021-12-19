import unittest
import puzzle as puz

class TestPuzzle(unittest.TestCase):

  def test_puzzle_parses_input(self):
    puzzle = puz.Puzzle()
    puzzle.process("""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
""")
    self.assertTrue((404,-588,-901) in puzzle.scanners[0])
    self.assertTrue((605,423,415) in puzzle.scanners[1])

  def test_puzzle_adds_all_points_to_empty_world(self):
    puzzle = puz.Puzzle()
    puzzle.process("""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
""")
    self.assertEqual(puzzle.ref, puzzle.scanners[0])
    self.assertEqual(set(puzzle.scanners[0]), puzzle.world)

  def test_puzzle_finds_overlaps_between_sets(self):
    puzzle = puz.Puzzle()
    puzzle.process("""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390
""")

    set1 = puzzle.scanners[0]
    set2 = puzzle.scanners[1]

    overlaps, mapped = puzzle.find_overlaps(set1, set2)

    self.assertEqual(overlaps, set([
      (-618,-824,-621),
      (-537,-823,-458),
      (-447,-329,318),
      (404,-588,-901),
      (544,-627,-890),
      (528,-643,409),
      (-661,-816,-575),
      (390,-675,-793),
      (423,-701,434),
      (-345,-311,381),
      (459,-707,401),
      (-485,-357,347),
    ]))



 
  def test_puzzle_can_offset_coords(self):
    puzzle = puz.Puzzle()
    point = [404, -588, -901]
    coords = [
      [686, 422, 578],
      [605, 423, 415],
      [515, 917, -361]
    ]

    offset = puzzle.offset(coords, point)
    self.assertEqual(offset, set([
      (686-404, 422+588, 578+901),
      (605-404, 423+588, 415+901),
      (515-404, 917+588, -361+901)
    ]))

  def test_puzzle_can_gen_rotations_of_point(self):
    puzzle = puz.Puzzle()
    point = [404, -588, -901]
    rotations = puzzle.rotations(point)
    self.assertEqual(set(rotations), set([
      ( 404,-588,-901),
      ( 404,-901, 588),
      ( 404, 588, 901),
      ( 404, 901,-588),

      (-404,-901,-588),
      (-404,-588, 901),
      (-404, 588,-901),
      (-404, 901, 588),

      (-588, 404, 901),
      (-588,-404,-901),
      (-588,-901, 404),
      (-588, 901,-404),

      ( 588, 404,-901),
      ( 588,-404, 901),
      ( 588, 901, 404),
      ( 588,-901,-404),

      (-901, 404,-588),
      (-901,-404, 588),
      (-901, 588, 404),
      (-901,-588,-404),

      ( 901, 404, 588),
      ( 901,-404,-588),
      ( 901,-588, 404),
      ( 901, 588,-404),
    ]))
    

if __name__ == '__main__':
    unittest.main()
