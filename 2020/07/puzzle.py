import re
import string

class Puzzle:

  def process(self, text):
    links = {}
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        key, klinks = self.parse_line(line)
        links[key] = klinks
    self.links = links
  
  def parse_line(self, line):
    bag, contents = line.split(' contain ')
    key = bag.replace(' bags', '')
    links = self.parse_links(contents)
    return (key, links)

  def parse_links(self, content):
    links = []
    contents = content.split(',')
    for bag in contents:
      bag = bag.strip().strip('.').replace(' bags', '').replace(' bag', '')
      if bag == 'no other':
        links.append((0, 'other'))
      else:
        match = re.match(r"([0-9]+)\s(.*)", bag)
        count = int(match.group(1))
        type = match.group(2)
        links.append((count, type))
    return links

  def eventually_contains(self, target, start):
    if start == target:
      return True
    if not self.links.has_key(start):
      return False
    links = self.links[start]
    for link in links:
      qty, bag = link
      if qty > 0:
        if self.eventually_contains(target, bag):
          return True
    return False

  def count_contains(self, start):
    count = 1
    if self.links.has_key(start):
      links = self.links[start]
      for link in links:
        num, bag = link
        print num, bag
        count = count + (num * self.count_contains(bag))
    return count

  def result1(self):
    bags = self.links.keys()
    total = 0
    for bag in bags:
      if bag != 'shiny gold':
        has_gold = self.eventually_contains('shiny gold', bag)
        if has_gold:
          total = total + 1
        print bag, has_gold
    print "Total", total

  def result(self):
    print "Bags in shiny gold", self.count_contains('shiny gold') - 1
  
  def dump_parse(self):
    for bag in self.links:
      print  bag + ' bags contain ' + self.str_links(self.links[bag]) + '.'
  
  def str_links(self, links):
    texts = []
    for link in links:
      text = ''
      qty, btype = link
      if qty == 0:
        text = 'no'
      else:
        text = str(qty)
      if qty == 1:
        text = text + ' ' + btype + ' bag'
      else:
        text = text + ' ' + btype + ' bags'
      texts.append(text)
    return ', '.join(texts)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
  #puz.dump_parse()
