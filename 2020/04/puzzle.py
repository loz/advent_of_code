import re

class Puzzle:

  REQ = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
  OPT = set(['cid'])

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
    return (self.valid_yr(passport['byr'], 1920, 2002) and
            self.valid_yr(passport['iyr'], 2010, 2020) and
            self.valid_yr(passport['eyr'], 2020, 2030) and
            self.valid_hgt(passport['hgt']) and
            self.valid_hcl(passport['hcl']) and
            self.valid_ecl(passport['ecl']) and
            self.valid_pid(passport['pid']))

  def valid_yr(self, byr, start, end):
   b = int(byr)
   return b >= start and b <= end

  def valid_hgt(self, hgt):
    match = re.match(r"([0-9]+)(in|cm)", hgt)
    if not match:
      return False
    val, unit =  match.groups()
    val = int(val)
    if unit == 'cm':
      return val >= 150 and val <= 193
    else:
      return val >= 59 and val <= 76

  def valid_hcl(self, hcl):
    match = re.match(r"^#[0-9a-f]{6}$", hcl) 
    return bool(match)

  def valid_pid(self, pid):
    match = re.match(r"^[0-9]{9}$", pid) 
    return bool(match)

  def valid_ecl(self, ecl):
    return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

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
