class Puzzle:

  def process(self, text):
    self.links = {}
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    left, right = line.split(' <-> ')
    links = right.split(', ')
    nid = int(left)
    nodes = map(lambda n: int(n), links)
    self.links[nid] = nodes

  def links_to(self, target, source, visited=[]):
    if target == source:
      return True
    nodes = self.links[source]
    for node in nodes:
      if node not in visited:
        if self.links_to(target, node, visited + [source]):
          return True
    return False

  def groups(self):
    groups = []
    maps = {}
    for key in self.links:
      if key in maps:
        group = maps[key]
      else:
        group = set([key])
      for node in self.links[key]:
        if node in maps:
          group |= maps[node]
        else:
          group |= set([node])
      for node in group:
        maps[node] = group
      print key, group
    groups = []
    for map in maps:
      group = list(maps[map])
      if group not in groups:
        groups.append(group)
    return groups

  def result(self):
    keys = self.links.keys()
    total = 0
    for key in keys:
      tozero = self.links_to(0, key)
      print key, tozero
      if tozero:
        total += 1
    print 'Total', total
    groups = self.groups()
    for group in groups:
      print group
    print len(groups)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
