class Puzzle:

  def process(self, text):
    self.outputs = []
    lines = text.split('\n')
    for line in lines:
      self.process_line(line)

  def process_line(self, line):
    if len(line) > 0:
      patterns, digits = line.split(' | ')
      print digits
      numbers = self.map_digits(digits)
      self.outputs.append(numbers)

  def map_digits(self, digits):
    digits = digits.split(' ')
    mapped = []
    for digit in digits:
      l = len(digit)
      if l == 2:
        mapped.append(1)
      elif l == 3:
        mapped.append(7)
      elif l == 4:
        mapped.append(4)
      elif l == 7:
        mapped.append(8)
    return mapped

  def result(self):
    total = 0
    for output in self.outputs:
      print output
      total += len(output)
    print 'Total 1, 4, 7, 8s:', total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
