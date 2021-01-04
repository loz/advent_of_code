class Puzzle:

  def process(self, text):
    self.nodes = {}
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    if '->' in line:
      left, right = line.split(' -> ')
      name, nid = self.process_node(left)
      children = right.split(', ')
    else:
      name, nid = self.process_node(line)
      children = []
    self.nodes[name] = (nid, children)

  def process_node(self, string):
    name, nid = string.split(' (')
    nid = nid.replace(')', '')
    return (name, int(nid))

  def find_root(self):
    for key in self.nodes:
      located = False
      for okey in self.nodes:
        _, children = self.nodes[okey]
        if key in children:
          located = True
          break
      if not located:
        return key

  def weight(self, nid):
    weight, children = self.nodes[nid]
    cweights = []
    for child in children:
      cweight, cblance = self.weight(child)
      cweights.append(cweight)
    weight += sum(cweights)
    balanced = len(set(cweights)) <= 1
    return (weight, balanced)

  def print_weights(self,nid):
    weight, balanced = self.weight(nid)
    _, children = self.nodes[nid]
    if not balanced:
      print nid, '=', weight, '[', ', '.join(children), ']'
      print self.nodes[nid][0],
      for child in children:
        cweight, _ = self.weight(child)
        print '+', cweight,
      print ''
    for child in children:
      self.print_weights(child)

  def result(self):
    bad = 'cumah'
    #bnode = self.nodes[bad]
    #self.nodes[bad] = (1801, bnode[1])
    root = self.find_root()
    print 'Root Node:', root
    self.print_weights(root)
    bnode = self.nodes[bad]
    bweight, bchildren = bnode
    print bad, bweight,
    for child in bchildren:
      cweight, _ = self.weight(child)
      print '+', cweight

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
