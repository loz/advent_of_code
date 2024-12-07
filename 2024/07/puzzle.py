import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.calibrations = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      total, vals = line.split(': ')
      vals = [int(n) for n in vals.split(' ')]
      self.calibrations.append((int(total), vals))

  def r_possible(self, op, total, vals):
    if len(vals) == 1:
      if total == vals[0]:
        return True
      else:
        return False
    
    v1, v2 = vals[0], vals[1]
    if op == '+':
      nv = v1 + v2
    elif op == '*':
      nv = v1 * v2
    elif op == '||':
      nv = int(str(v1) + str(v2))

    nvals = [nv] + vals[2:]
    return self.r_possible('+', total, nvals) or \
           self.r_possible('*', total, nvals) or \
           self.r_possible('||', total, nvals)

  def possible(self, calibration):
    total, vals = calibration
    return self.r_possible('+', total, vals) or \
           self.r_possible('*', total, vals) or \
           self.r_possible('||', total, vals)

  def result(self):
    total = 0
    for cal in self.calibrations:
      ispos = self.possible(cal)
      if ispos:
        print(cal, Fore.GREEN + 'Possible' + Fore.RESET)
        total += cal[0]
      else:
        print(cal)
    print('Total Calibration:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
