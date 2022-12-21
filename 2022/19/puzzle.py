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
    return (costs[0] <= resources[0] and costs[1] <= resources[1] and costs[2] <= resources[2])

  def build(self, costs, resources):
    return (resources[0]-costs[0],resources[1]-costs[1],resources[2]-costs[2], resources[3])

  def gen_choices(self, blueprint, resources):
    costs = self.blueprints[blueprint]
    options = [None]
    geo = costs["geode"]
    if self.can_afford(geo, resources):
      #build it!
      return ["geode"]
    for item in ["ore", "clay", "obsidian"]:
      needs = costs[item]
      if self.can_afford(needs, resources):
        options.append(item)
    return options
    
  def collect(self, resources, robots):
    return(resources[0] + robots["ore"], resources[1] + robots["clay"], resources[2] + robots["obsidian"], resources[3] + robots["geode"])

  def build(self, robot, resources, robots, idx):
    costs = self.blueprints[idx][robot]
    resources = (resources[0]-costs[0], resources[1]-costs[1], resources[2]-costs[2], resources[3])

    nrobots = robots.copy()
    count = nrobots.get(robot, 0)
    nrobots[robot] = count + 1
    #print 'New ', robot, 'you now have', nrobots[robot]
    return nrobots, resources

  def min_viable(self, idx):
    costs = self.blueprints[idx]

    obreq = costs["geode"][2]
    obsidian = 0
    timestamp = 24
    for i in range(obreq):
      offset = timestamp-(obreq/(i+1))-(i+1)
      if offset >= obsidian:
        obsidian = offset
    clayreq = costs["obsidian"][1]
    clay = 0
    maxclay = 0
    for i in range(clayreq):
      offset = obsidian-(clayreq/(i+1))-(i+1)
      if offset >= clay:
        clay = offset
        if (i+1) > maxclay:
          maxclay = i+1
    orreq = costs["clay"][0]
    orcost = costs["ore"][0]
    maxore = 0
    maxclay = 0
    for req in costs:
      maxore = max(maxore, costs[req][0])
      maxclay = max(maxclay, costs[req][1])
    return (obsidian+1, clay+1, maxclay+1, maxore+1)

  def run_blueprint(self, idx, timelimit=24):
    viable = self.min_viable(idx)
    print viable, self.blueprints[idx]
    limits = {
      "ore": viable[3],
      "clay": viable[2],
      "obsidian": 9999,
      "geode": 9999
    }
    print 'Limits', limits
    bestdepth = {}
    visited = {}
    maxgeod = 0
    maxrobot = []
    allpaths = []
    best = None
    robots = {"ore":1, "clay":0, "obsidian":0, "geode":0}
    resources = (0, 0, 0, 0)
    #tovisit = [(robots, resources, 0, [])]
    tovisit = [(robots, resources, 0)]
    while tovisit:
      #robots, resources, timer, path = tovisit.pop()
      robots, resources, timer = tovisit.pop()
      item = (robots["ore"], robots["clay"], robots["obsidian"], robots["geode"], resources, timer)
      if visited.get(item, False):
        continue
      else:
        visited[item] = True
      if bestdepth.get(timer, 0) > resources[3]: #We have better at depth seen before
        #print 'Culling Poorer Path'
        continue
      else:
        #print 'Best at depth', timer, resources[3]
        bestdepth[timer] = resources[3]
      if timer == timelimit:
        if resources[3] > maxgeod:
          maxgeod = resources[3]
          #maxrobot = path
          #best = robots
        #allpaths.append(path)
        continue
      #print '== Minute ', timer, '=='
      #if timer == viable[1] and robots["clay"] == 0:
      #  #print 'Culling For Clay'
      #  continue
      #if timer == viable[0] and robots["obsidian"] == 0:
      #  #print 'Culling for Obsidian'
      #  continue
      options = self.gen_choices(idx, resources)
      for option in options:
        if option == None: #Wait option
          nrobots = robots.copy()
          nresources = self.collect(resources, robots)
          #tovisit.append((nrobots, nresources, timer+1, path + [(nrobots, nresources)]))
          tovisit.append((nrobots, nresources, timer+1))
        else:
          if robots.get(option, 0) < limits[option]:
            nrobots, nresources = self.build(option, resources, robots, idx)
            nresources = self.collect(nresources, robots)
            #tovisit.append((nrobots, nresources, timer+1, path + [(robots, nresources)]))
            tovisit.append((nrobots, nresources, timer+1))

    #for path in allpaths:
    #  print '='*80
    #  minute = 1
    #  for step in path:
    #    print 'Minute', minute, step
    #    minute += 1
    #  print '===='

    #print 'Max', maxgeod
    #minute = 1
    #for step in maxrobot:
    #  print 'Minute', minute, step
    #  minute += 1
    #print '===='
    #print 'Best', best, maxgeod
    return maxgeod

  def result_x(self):
    for blueprint in range(len(self.blueprints)):
      print blueprint, self.min_viable(blueprint)

  def result(self):
    blueprint = 0
    total = 0
    for blueprint in range(len(self.blueprints)):
    #for blueprint in [1]:
      print 'Running BP:', blueprint+1
      val = self.run_blueprint(blueprint)
      print val, 'quality', (blueprint+1)*val
      total += ((blueprint+1)*val)
    print 'Total', total

  def result2(self):
    blueprint = 0
    total = 0
    #for blueprint in range(len(self.blueprints)):
    for blueprint in [0,1,2]:
      print 'Running BP:', blueprint+1
      val = self.run_blueprint(blueprint, 32)
      print val, 'quality', (blueprint+1)*val
      total += ((blueprint+1)*val)
    print 'Total', total

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
