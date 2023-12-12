import sys

class Puzzle:

  def process(self, text):
    self.records = []
    self.checks = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      lhs, rhs = line.split(' ')
      self.records.append(lhs)
      check = [int(n) for n in rhs.split(',')]
      self.checks.append(check)

  def r_possible(self, records, checks, indent=''):
    #Consume OK
    while(records != [] and records[0] == '.'):
      records = records[1:]

    if(len(records) == 0):
      if(len(checks) == 0):
        return 1
      else:
        return 0

    if(len(checks) == 0):
      if '#' in records:
        return 0 #Not posisble, no more block are to be present

    if(records[0] == '?'):
      #Try as '.' + #Try as '#'
      return self.r_possible(records[1:], checks, indent + 'a ') + self.r_possible(['#'] + records[1:], checks, indent + 'b ')
    else:
      #We are supposed to be AT a run of run items
      run, checks = checks[0], checks[1:]
      #print(indent, '>>', records, run, checks)
      if len(records) < run:
        return 0 #Not possible
      block = records[0:run]
      records = records[run:]
      #print(indent, '}}', block, records)
      if '.' in block:
        return 0 #Not possible as block includes '.'
      #Block matches, only if POST block is '.'
      if(records == []):
        if checks == []:
          return 1 #Possible
        else:
          return 0 #Not possible
      elif records[0] == '#':
        return 0 #Not possible as block too large
      #Regardless of ? or . ? must be a ., so possbile
      # if remainder matches the checks
      return self.r_possible(records[1:], checks, indent + ' ')



  def possible(self, records, checks):
    chs = [ch for ch in records]
    return self.r_possible(chs, checks)

  def result(self):
    self.result1()

  def result1(self):
    total = 0
    for n in range(len(self.records)):
      records = self.records[n]
      checks = self.checks[n]
      p = self.possible(records, checks)
      total += p
      print(records, checks, p)
    print('Total', total)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
