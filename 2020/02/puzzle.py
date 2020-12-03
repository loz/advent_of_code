def parse_line(line):
  if len(line) == 0:
    return None
  parts = line.split(' ')
  size, char, password = parts
  sizes = size.split('-')
  minS, maxS = sizes
  char = char[0]
  return ((int(minS), int(maxS), char), password)

class Puzzle:

  def process(self, text):
    self.passwords = map(lambda n: parse_line(n), text.split('\n'))

  def validPassword(self, password):
    rule, password = password
    minS, maxS, char = rule
    occurs = password.count(char)
    return (occurs >= minS and occurs <= maxS)

  def validPassword2(self, password):
    rule, password = password
    minS, maxS, char = rule
    if minS > len(password) or maxS > len(password):
      return False
    atMin = password[minS-1] == char
    atMax = password[maxS-1] == char
    if atMin and atMax:
      return False
    return atMin or atMax

  def result(self):
    totalValid = 0
    for password in self.passwords:
      if password != None:
        valid = self.validPassword2(password)
        if valid:
          totalValid = totalValid + 1
        print password, valid
    print "Total Good", totalValid

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
