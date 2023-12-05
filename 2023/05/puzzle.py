import sys

class Puzzle:

  def process(self, text):
    self.seeds = []
    self.maps = {}
    lines = text.split('\n')
    lines = self.process_seeds(lines)
    self.process_maps(lines)

  def process_seeds(self, lines):
    first, rest = lines[0], lines[1:]
    first = first.replace('seeds: ', '')
    seeds = first.split(' ')
    for s in seeds:
      if s != '':
        self.seeds.append(int(s))
    return rest

  def process_maps(self, lines):
    state = None
    src = None
    dst = None
    mappings = []
    for line in lines:
      if line == '':
        if state != None:
          self.maps[src] = (dst, mappings)
        state = None
        #print('Next')
      elif state == None:
        src_to_dst = line.replace(' map:', '')
        src, dst = src_to_dst.split('-to-')
        #print('Map', src, dst)
        state = 'Map'
        mappings = []
      elif state == 'Map':
        nums = line.split(' ')
        ns = []
        for n in nums:
          if n != '':
            ns.append(int(n))
        #print('Numbers', ns)
        mappings.append(ns)
    if state != None:
      self.maps[src] = (dst, mappings)

  def map(self, src, num):
    dst, maps = self.maps[src]
    for r in maps:
      dstart, sstart, size = r
      if num >= sstart and num < sstart+size:
        #print('In', sstart, sstart+size)
        diff = (num-sstart)
        return (dst, dstart+diff)
    #No match, return original number
    return (dst, num)

  def gen_range(self, maps):
    maps = sorted(maps, key = lambda x: x[1])
    #print('Sorted', maps)
    newmaps = []
    mmin = 0
    mmax = 9_999_999_999_999_999
    while(maps):
      curmap = maps.pop(0)
      cdest, cstart, size = curmap
      if mmin < cstart:
        glen = cstart-mmin
        #print('Gap', mmin, glen)
        newmaps.append([mmin, mmin, glen])
        #print('Curmap', curmap)
        newmaps.append(curmap)
        mmin = cstart+size
      elif mmin == cstart:
        newmaps.append(curmap)
        mmin = cstart+size
        


    glen = mmax-mmin-1
    #print('Gap', mmin, glen)
    newmaps.append([mmin, mmin, glen])
    #print('Curmap', curmap)
    return newmaps

  def range_map(self, src, sstart, send):
    dst, maps = self.maps[src]
    gapmaps = self.gen_range(maps)
    ranges = []
    #print('Search', gapmaps, 'vs', sstart, send)
    #find first range inclusive
    found = False
    while(not found):
      mmap = gapmaps.pop(0)
      _, mstart, msize = mmap
      if sstart >= mstart and sstart <= mstart+msize:
        ranges.append(mmap)
        found = True
    #find last range inclusive
    while(gapmaps):
      mmap = gapmaps.pop(0)
      _, mstart, msize = mmap
      if send > mstart:
        ranges.append(mmap)
    #print('Ranges', ranges)
    mranges = []
    #forall return mapped ranges
    if len(ranges) == 1:
      #Map range of src and end values
      cmap = ranges[0]
      dstart, rstart, size = cmap
      diff1 = sstart-rstart
      diff2 = send-rstart
      r = (dstart+diff1, dstart+diff2)
      #print('One', cmap, r)
      mranges.append(r)
      pass
    else: #start, end + map internals
      #map src start in first to end of first
      first = ranges.pop(0)
      dstart, rstart, size = first
      diff1 = sstart-rstart
      diff2 = size-1
      r = (dstart+diff1, dstart+diff2)
      #print('First', first, r)
      mranges.append(r)

      last = ranges.pop()
      #map all internal ranges start-end
      for r in ranges:
        dstart, rstart, rlen = r
        diff1 = 0
        diff2 = rlen-1  
        mr = (dstart+diff1, dstart+diff2)
        #print('Range', r, mr)
        mranges.append(mr)

      #map start of last to src end
      dstart, rstart, size = last
      diff1 = 0
      diff2 = send-rstart
      r = (dstart+diff1, dstart+diff2)
      #print('Last', last, r)
      mranges.append(r)
    print(dst, mranges)
    return (dst, mranges)

  def traverse(self, key, val):
    if(self.maps.get(key, None)):
      sys.stdout.write("%s %d, " % (key, val))
      nkey, nval = self.map(key, val)
      return self.traverse(nkey, nval)
    else:
      sys.stdout.write("%s %d\n" % (key, val))
      return val

  def range_traverse(self, key, smin, smax, indent=''):
    if(self.maps.get(key, None)):
      sys.stdout.write("%s%s %d-%d, " % (indent, key, smin, smax))
      dst, ranges = self.range_map(key, smin, smax)
      #print('Ranges', ranges)
      mins = []
      for r in ranges:
        mins.append(self.range_traverse(dst, r[0], r[1], indent+' '))
      return min(mins)
    else:
      sys.stdout.write("%s%s %d-%d\n" % (indent, key, smin, smax))
      return smin

  def result(self):
    #self.result_brute()
    self.result_range()

  def result_brute(self):
    lowest = 9_999_999_999_999_999
    pairs = []
    for n in range(len(self.seeds)):
      if n % 2 == 0:
        pairs.append((self.seeds[n], self.seeds[n+1]))
    print(pairs)
    for pair in pairs:
      for s in range(pair[0], pair[0]+pair[1]):
        n = self.traverse('seed', s)
        if n < lowest:
          lowest = n
    print('Lowest', lowest)
    
  def result_range(self):
    lowest = 9_999_999_999_999_999
    pairs = []
    for n in range(len(self.seeds)):
      if n % 2 == 0:
        pairs.append((self.seeds[n], self.seeds[n+1]))
    for pair in pairs:
      print('Range', pair[0], pair[0]+pair[1])
      smin = pair[0]
      smax = pair[0]+pair[1]-1 #inclusive
      n = self.range_traverse('seed', smin, smax)
      if n < lowest:
        lowest = n
    print('Lowest', lowest)

  def result1(self):
    lowest = 9_999_999_999_999_999
    for seed in self.seeds:
      n = self.traverse('seed', seed)
      if n < lowest:
        lowest = n
    print('Lowest', lowest)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
