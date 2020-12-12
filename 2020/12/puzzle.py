class Puzzle:

  def process(self, text):
    self.x = 0
    self.y = 0
    self.waypoint_x = 10
    self.waypoint_y = -1

    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.process_line(line)

  def process_line(self, line):
    action = line[0]
    value = int(line[1:])
    if action == 'N':
      self.waypoint_y -= value
    elif action == 'S':
      self.waypoint_y += value
    elif action == 'E':
      self.waypoint_x += value
    elif action == 'W':
      self.waypoint_x -= value
    elif action == 'F':
      self.x += self.waypoint_x * value
      self.y += self.waypoint_y * value
    elif action == 'B':
      self.x -= self.waypoint_x * value
      self.y -= self.waypoint_y * value
    elif action == 'R':
      n = value / 90
      for i in range(0,n):
        newbearing = (-1 * self.waypoint_y, self.waypoint_x)
        self.waypoint_x, self.waypoint_y = newbearing
    elif action == 'L':
      n = value / 90
      for i in range(0,n):
        newbearing = (self.waypoint_y, -1 * self.waypoint_x)
        self.waypoint_x, self.waypoint_y = newbearing

  def result(self):
    print self.x, self.y
    print "Distance:", abs(self.x) + abs(self.y)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
