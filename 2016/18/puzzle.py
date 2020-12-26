class Puzzle:

  def genline(self, line):
    parts = [ch for ch in line]
    newparts = []
    for i in range(len(parts)):
      left, center, right = self.neighbours(i, parts)
      if left == center == '^' and right == '.':
        newparts.append('^')
      elif center == right == '^' and left == '.':
        newparts.append('^')
      elif left == '^' and center == right == '.':
        newparts.append('^')
      elif right == '^' and center == left == '.':
        newparts.append('^')
      else:
        newparts.append('.')
    return ''.join(newparts)

  def neighbours(self, col, parts):
    if col == 0:
      return ('.', parts[col], parts[col+1])
    elif col == len(parts)-1:
      return (parts[col-1], parts[col], '.')
    else:
      return (parts[col-1], parts[col], parts[col+1])
   
  def numsafe(self, line):
    return line.count('.')

  def result(self, line, rows=None):
    total = 0
    if rows == None:
      rows = len(line)
    for i in range(rows):
      safe = self.numsafe(line)
      total += safe
      #print line, safe, '(', i+1, ')'
      line = self.genline(line)
    print 'Total Safe Tiles:', total


if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  inp = inp.strip()
  puz.result(inp, 400000)
