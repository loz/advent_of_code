import unittest
import puzzle as puz

INPUT = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

VALID = {
  'byr': '2002',
  'iyr': '2010',
  'eyr': '2020',
  'hgt': '60in',
  'hcl': '#aaaaaa',
  'ecl': 'brn',
  'pid': '000000001'
}

class TestPuzzle(unittest.TestCase):

  def test_splits_into_passports(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertEquals(len(puzzle.passports), 4)

  def test_parses_parts(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    first = puzzle.passports[0]
    self.assertEqual(first['cid'], '147')
    self.assertEqual(first['pid'], '860033327')
  
  def test_can_check_valid(self):
    puzzle = puz.Puzzle()
    puzzle.process(INPUT)
    self.assertTrue(puzzle.valid(puzzle.passports[0]))
    self.assertFalse(puzzle.valid(puzzle.passports[1]))
    self.assertTrue(puzzle.valid(puzzle.passports[2]))
    self.assertFalse(puzzle.valid(puzzle.passports[3]))

  def test_can_validate_byr(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['byr'] = '1919'
    self.assertFalse(puzzle.valid(passport))
    passport['byr'] = '1920'
    self.assertTrue(puzzle.valid(passport))
    passport['byr'] = '2002'
    self.assertTrue(puzzle.valid(passport))
    passport['byr'] = '2003'
    self.assertFalse(puzzle.valid(passport))

  def test_can_validate_iyr(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['iyr'] = '2009'
    self.assertFalse(puzzle.valid(passport))
    passport['iyr'] = '2010'
    self.assertTrue(puzzle.valid(passport))
    passport['iyr'] = '2020'
    self.assertTrue(puzzle.valid(passport))
    passport['iyr'] = '2021'
    self.assertFalse(puzzle.valid(passport))

  def test_can_validate_eyr(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['eyr'] = '2019'
    self.assertFalse(puzzle.valid(passport))
    passport['eyr'] = '2020'
    self.assertTrue(puzzle.valid(passport))
    passport['eyr'] = '2030'
    self.assertTrue(puzzle.valid(passport))
    passport['eyr'] = '2031'
    self.assertFalse(puzzle.valid(passport))

  def test_can_validate_hgt(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['hgt'] = '190in'
    self.assertFalse(puzzle.valid(passport))
    passport['hgt'] = '76in'
    self.assertTrue(puzzle.valid(passport))
    passport['hgt'] = '193cm'
    self.assertTrue(puzzle.valid(passport))
    passport['hgt'] = '194cm'
    self.assertFalse(puzzle.valid(passport))
    passport['hgt'] = '193'
    self.assertFalse(puzzle.valid(passport))

  def test_can_validate_hcl(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['hcl'] = '$aaaaaa'
    self.assertFalse(puzzle.valid(passport))
    passport['hcl'] = '#0f0f0f'
    self.assertTrue(puzzle.valid(passport))
    passport['hcl'] = '#000000'
    self.assertTrue(puzzle.valid(passport))
    passport['hcl'] = '#gggggg'
    self.assertFalse(puzzle.valid(passport))
    passport['hcl'] = '#aaaaaaa'
    self.assertFalse(puzzle.valid(passport))

  def test_can_validate_ecl(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['ecl'] = 'wat'
    self.assertFalse(puzzle.valid(passport))
    passport['ecl'] = 'blu'
    self.assertTrue(puzzle.valid(passport))
    passport['ecl'] = 'amb'
    self.assertTrue(puzzle.valid(passport))
    passport['ecl'] = 'grn'
    self.assertTrue(puzzle.valid(passport))
    passport['ecl'] = 'hzl'
    self.assertTrue(puzzle.valid(passport))
    passport['ecl'] = 'oth'
    self.assertTrue(puzzle.valid(passport))

  def test_can_validate_pid(self):
    puzzle = puz.Puzzle()
    self.assertTrue(puzzle.valid(VALID))
    passport = VALID.copy()
    passport['pid'] = 'asdasdadas'
    self.assertFalse(puzzle.valid(passport))
    passport['pid'] = '100000000'
    self.assertTrue(puzzle.valid(passport))
    passport['pid'] = '000555000'
    self.assertTrue(puzzle.valid(passport))
    passport['pid'] = '0000000001'
    self.assertFalse(puzzle.valid(passport))
    passport['pid'] = '1000000000'
    self.assertFalse(puzzle.valid(passport))

if __name__ == '__main__':
    unittest.main()
