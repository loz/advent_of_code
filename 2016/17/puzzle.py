import hashlib

MAP="""#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |  
####### V"""

DELTA = {
  'U': ( 0,-1),
  'D': ( 0, 1),
  'L': (-1, 0),
  'R': ( 1, 0)
}

HASHPOS = {
  'U': 0,
  'D': 1,
  'L': 2,
  'R': 3
}

class Puzzle:

  def process(self, text):
    pass

  def gen_paths(self, loc, path):
    #print 'Gen', loc, path
    x, y = loc
    options = []
    md5hash = hashlib.md5(path).hexdigest()
    for direction in DELTA:
      dx, dy = DELTA[direction]
      xdx = x + dx
      ydy = y + dy
      if xdx >= 0 and xdx <= 3 and ydy >= 0 and ydy <= 3:
        pos = HASHPOS[direction]
        if md5hash[pos] in ['b', 'c', 'd', 'e', 'f']:
                options.append(((xdx,ydy), path + direction))
    return options

  def result(self, passcode):
    discovered = {}
    head = [((0, 0), passcode)]
    tail = []
    while len(head) > 0:
      loc, path = head.pop(0)
      if loc == (3,3):
        print 'HERE!',
        print path
        return
      options = self.gen_paths(loc, path)
      for option in options:
        if not discovered.has_key(option):
          discovered[option] = True
        tail.append(option)
      if len(head) == 0:
        head = tail
        tail = []
      print loc, path

  def result2(self, passcode):
    discovered = {}
    paths = []
    head = [((0, 0), passcode)]
    while len(head) > 0:
      loc, path = head.pop(0)
      if loc == (3,3):
        paths.append(path[len(passcode):])
      else:
        options = self.gen_paths(loc, path)
        for option in options:
          head.append(option)
    paths.sort(key=lambda p: len(p), reverse=True)
    longest = paths[0]

    print 'A Longest', longest
    print 'Length', len(longest)

if __name__ == '__main__':
  puz = Puzzle()
  #puz.result('ihgpwlah')
  puz.result2('ihgpwlah')
  #puz.result('kglvqrro')
  puz.result2('kglvqrro')
  #puz.result('ulqzkmiv')
  puz.result2('ulqzkmiv')
  #puz.result('pvhmgsws')
  puz.result2('pvhmgsws')
