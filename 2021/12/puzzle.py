class Puzzle:

  def process(self, text):
    self.nodes = {}
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if len(line) > 0:
      self.link_nodes(line)

  def link_nodes(self, node):
    left, right = node.split('-')
    if left in self.nodes:
      self.nodes[left].add(right)
    else:
      self.nodes[left] = set([right])
    if right in self.nodes:
      self.nodes[right].add(left)
    else:
      self.nodes[right] = set([left])

  def build_paths(self):
    curnode = 'start'
    return self._paths_from_node(curnode, [], None)

  def _paths_from_node(self, node, visited, twice):
    if node == 'end':
      return [visited + ['end']]
    options = self.nodes[node]
    paths = []
    for opt in options:
      if opt in visited and self.small_cave(opt):
        if opt == 'start' or twice != None:
          pass
        else:
          print 'Again', opt, visited
          paths += self._paths_from_node(opt, visited + [node], opt)
      else:
        paths += self._paths_from_node(opt, visited + [node], twice)
    return paths
  
  def small_cave(self, label):
    return label == label.lower()

  def result(self):
    paths = self.build_paths()
    for path in paths:
      print path
    print 'Total Paths', len(paths)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
