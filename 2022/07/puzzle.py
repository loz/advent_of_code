import sys

class FSNode:
  def __init__(self, name, parent=None, size=None):
    self._totalSize = None
    self.name = name
    self.size = size
    self.parent = parent
    self.files = []
    self.dirs  = []

  def totalSize(self):
    if self._totalSize: #Cache
      return self._totalSize
    size = 0
    for f in self.files:
      size += f.size
    for d in self.dirs:
      size += d.totalSize()
    self._totalSize = size
    return size
  
  def dump(self, indent = ''):
    print indent, self.name, ':--'
    for f in self.files:
      print indent, ' ', f.name, f.size
    for d in self.dirs:
      d.dump(indent = indent + '  ')

class Puzzle:

  def process(self, text):
    self.root = FSNode('/')
    self.curnode = self.root

    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      if line.startswith('$'):
        self.process_command(line)
      else:
        self.process_listing(line)

  def process_command(self, line):
    params = line.split(' ')
    op = params[1]
    if op == 'ls':
      pass
    elif op == 'cd':
      target = params[2]
      if target == '..':
        self.curnode = self.curnode.parent
      elif target == '/':
        self.curnode = self.root
      else:
        options = filter(lambda x: x.name == target, self.curnode.dirs)
        self.curnode = options[0]

  def process_listing(self, line):
    left, right = line.split(' ')
    if left == 'dir': #directory
      dNode = FSNode(right, parent=self.curnode)
      self.curnode.dirs.append(dNode)
    else:
      size = int(left)
      fNode = FSNode(right, parent=self.curnode, size=size)
      self.curnode.files.append(fNode)

  def dump_fs(self):
    self.root.dump()

  def walkdirs(self, node):
    dirs = [] + node.dirs
    for d in node.dirs:
      childs = self.walkdirs(d)
      dirs += childs
    return dirs

  def result(self):
    print 'Walking Dirs'
    dirs = self.walkdirs(self.root)
    total = 0
    for d in dirs:
      dsize = d.totalSize()
      print d.name, 'TotalSize', d.size
      if dsize <= 100000:
        print 'YES'
        total += dsize
    print 'Sum', total

  def result2(self):
    dirs = self.walkdirs(self.root)
    print 'Used', self.root.totalSize()
    target = self.root.totalSize() - (70000000 - 30000000)
    print 'Free Target', target
    possible = filter(lambda x: x.totalSize() >= target, dirs)
    for d in possible:
      print '-', d.name, d.totalSize()
    win = min(possible, key=lambda x: x.totalSize())
    print 'Winner', win.name, win.totalSize()

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result2()
