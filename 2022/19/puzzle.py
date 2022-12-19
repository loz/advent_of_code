import sys
import re

class Puzzle:

  def process(self, text):
    self.blueprints = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      left, right = line.split(':')
      costs = {}
      parts = right.split('.')
      for part in parts:
        if part != '':
          item, cost = self.process_part(part)
          costs[item] = cost
      self.blueprints.append(costs)
  
  def process_part(self, part):
    ore = 0
    clay = 0
    obsidian = 0
    match = re.search('Each (.+) robot costs', part)
    name = match.group(1)

    match = re.search('(\d+) ore', part)
    if match:
     ore = int(match.group(1))

    match = re.search('(\d+) clay', part)
    if match:
     clay = int(match.group(1))

    match = re.search('(\d+) obsidian', part)
    if match:
     obsidian = int(match.group(1))

    return (name, (ore, clay, obsidian))

  def can_afford(self, costs, resources):
    ca, cb, cc   = costs
    ra, rb, rc,_ = resources
    return (ca <= ra and cb <= rb and cc <= rc)

  def build(self, costs, resources):
    ca, cb, cc   = costs
    ra, rb, rc, rd  = resources
    return (ra-ca, rb-cb, rc-cc, rd)

  def gen_choices(self, blueprint, resources):
    costs = self.blueprints[blueprint]
    options = []
    geo = costs["geode"]
    if self.can_afford(geo, resources):
      #build it!
      return ["geode"]
    if resources[2] >= geo[2]:
      return [None] #Wait for resources

    obs = costs["obsidian"]
    if self.can_afford(obs, resources):
      #build it!
      return ["obsidian"]
    if resources[1] >= obs[1]:
      return [None] #Wait for resources
    for item in ["ore", "clay"]:
      needs = costs[item]
      if self.can_afford(needs, resources):
        options.append(item)
    options.append(None)
    return options

  def collect(self, resources, robots):
    amounts = {
      "ore":resources[0],
      "clay":resources[1],
      "obsidian":resources[2],
      "geode":resources[3],
    }
    for robot in robots.keys():
      amounts[robot] += robots[robot]
      print robots[robot], robot, 'collect, you have now have', amounts[robot]
    return (amounts['ore'], amounts['clay'], amounts['obsidian'], amounts['geode'])

  def build(self, robot, resources, robots, idx):
    amounts = {
      "ore":resources[0],
      "clay":resources[1],
      "obsidian":resources[2],
    }
    costs = self.blueprints[idx][robot]
    resources = (resources[0]-costs[0], resources[1]-costs[1], resources[2]-costs[2], resources[3])

    nrobots = robots.copy()
    count = nrobots.get(robot, 0)
    nrobots[robot] = count + 1
    print 'New ', robot, 'you now have', nrobots[robot]
    return nrobots, resources


  def run_blueprint(self, idx):
    robots = {"ore":1}
    resources = (0, 0, 0, 0)
    tovisit = [(robots, resources, 0)]
    while tovisit:
      robots, resources, timer = tovisit.pop()
      if timer == 24:
        continue
      print '== Minute ', timer, '=='
      resources = self.collect(resources, robots)
      options = self.gen_choices(idx, resources)
      for option in options:
        if option == None: #Wait option
          tovisit.append((robots, resources, timer+1))
        else:
          nrobots, resources = self.build(option, resources, robots,idx)
          tovisit.append((nrobots, resources, timer+1))

  def result(self):
    blueprint = 1
    self.run_blueprint(blueprint)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()