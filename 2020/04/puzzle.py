import re

class Puzzle:

  REQ = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
  OPT = set(['cid'])

  RULES = {
    'byr': r"^(19[2-9][0-9]|200[0-2])$",
    'iyr': r"^20(1[0-9]|20)$",
    'eyr': r"^20(2[0-9]|30)$",
    'hgt': r"^(1([5-8][0-9]|9[0-3])cm)|((59|6[0-9]|7[0-6])in)$",
    'hcl': r"^#[0-9a-f]{6}$",
    'ecl': r"^(amb|blu|brn|gry|grn|hzl|oth)$",
    'pid': r"^[0-9]{9}$"
  }

  def process(self, text):
    self.passports = []
    lines = text.split('\n')
    passport = ''
    for line in lines:
      line = line.strip()
      if line == '':
        parts = passport.split(' ')
        doc = {}
        for part in parts:
          if part.strip() != '':
            elems = part.split(':')
            k = elems[0]
            v = elems[1]
            doc[k] = v
        self.passports.append(doc)
        passport = ''
      else:
        passport = passport + ' '  + line

  def valid(self, passport):
    passkeys = set(passport.keys())
    mandleft = Puzzle.REQ - passkeys
    if len(mandleft) != 0:
      return False
    for key in Puzzle.RULES:
      rule = Puzzle.RULES[key]
      if not re.match(rule, passport[key]):
        return False 
    return True

  def result(self):
    totalValid = 0
    for passport in self.passports:
      valid = self.valid(passport)
      print passport, valid
      if valid:
        totalValid = totalValid + 1
    print "Total Valid", totalValid

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
