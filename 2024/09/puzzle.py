import sys
from colorama import Fore

class Puzzle:

  def process(self, text):
    self.diskmap = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      for ch in line:
        self.diskmap.append(int(ch))

  def super_defrag(self, blocks):
    #print('DEFRAG:', blocks)
    maxblock = 0
    for b in blocks:
      if b[0] != None and b[0] > maxblock:
        maxblock = b[0]
    #print('Defragging from ', maxblock, 'down')
    while maxblock >= 0:
      #Find the block
      blockloc = None
      for idx, b  in enumerate(blocks):
        if b[0] == maxblock:
          blockloc = idx
          break
      #print('Seeking For', maxblock, '>', blockloc, '=', blocks[blockloc])
      target = blocks[blockloc]
      #Find the available gap
      insertloc = None
      for idx, b  in enumerate(blocks):
        if b[0] == None and b[1] >= target[1]:
          insertloc = idx
          break
      #print('Found For', insertloc, '>>', blocks[insertloc])

      extraspace = 0

      if insertloc and insertloc < blockloc:
        gap = blocks[insertloc]
        left = blocks[:insertloc]
        mid = blocks[insertloc+1:blockloc]
        right = blocks[blockloc+1:]
        if gap[1] > target[1]:
          space = [(None, gap[1]-target[1])]
        else:
          space = []
        extraspace = target[1]
        if mid == []:
          mid = space
          space = []

        if right != [] and mid != [] and right[0][0] == None and mid[-1][0] == None:
          #None either side of move
          extra = [(None, right[0][1] + mid[-1][1] + extraspace)]
          right = right[1:]
          mid = mid[:-1]
        else:
          if right != [] and right[0][0] == None:
            right[0] = (None, right[0][1] + extraspace)
            extra = []
          elif mid != [] and mid[-1][0] == None:
            mid[-1] = (None, mid[-1][1] + extraspace)
            extra = []
          else:
            extra = [(None, extraspace)]
        blocks = left + [target] +space + mid + extra + right
      #print('DEFRAG @', maxblock, '->', self.str_debug(blocks))
      maxblock-= 1


    return blocks

  def defrag(self, blocks):

    #print('DEFRAG:', blocks)
    did = False
    newblocks = []
    #Find the first gap
    firstgap = None
    for i, block in enumerate(blocks):
      if block[0] == None:
        #found
        firstgap = i
        break

    #TODO: if firstgap == None, No defrag
    lastblock = None
    for i in range(len(blocks)-1, 0, -1):
      if blocks[i][0] != None:
        #found
        lastblock = i
        break

    left = blocks[:firstgap]
    midd = blocks[firstgap+1:lastblock]
    gap = blocks[firstgap]
    endspace = blocks[lastblock+1:]

    chunk = blocks[lastblock]
    #print(left, '<<', gap, '>>',  midd, '<<', chunk, '>>',  endspace)
    if len(left)-1 == lastblock:
      return False, blocks

    did = True
    #If left of gap is same blockid
    leftof = left[-1]
    if leftof[0] == chunk[0]:
      left[-1] = (leftof[0], leftof[1]+1)
      newchunk = []
    else:
      newchunk = [(chunk[0], 1)]

    #If a gap is still open
    if gap[1] > 1:
      newgap = [(None, gap[1]-1)]
    else:
      newgap = []

    extraspace = 1
    #If chunk remaining:
    if chunk[1] > 1:
      newend = [(chunk[0], chunk[1]-1)]
    else:
      #If gap on left, merge with end
      if midd == []:
        if gap[1] > 1:
          extraspace = gap[1]
          newgap = []

      #if midd[-1] != [] and midd[-1][0] == None:
      #  pass
      newend = []
    #If endspace is already as space
    if len(endspace) == 0:
      newspace = [(None, extraspace)]
    else:
      endspace = [(None, endspace[0][1]+extraspace)]
      newspace = []

    newblocks = left + newchunk + newgap + midd + newend + newspace + endspace
    return did, newblocks

  def decompress(self, diskmap):
    blocks = []
    index = 0
    isblock = True
    for n in diskmap:
      if isblock:
        if n > 0:
          blocks.append((index, n))
        isblock = False
        index += 1
      else:
        if n > 0:
          blocks.append((None, n))
        isblock = True
    return blocks

  def checksum(self, blocks):
    idx = 0
    csum = 0
    for b in blocks:
      bid, count = b
      if bid == None:
        idx += count
      else:
        for n in range(count):
          csum += (bid * idx)
          idx += 1
    return csum

    return 0

  def str_debug(self, block):
    text = ""
    for b in block:
      idx, count = b
      if idx == None:
        text += '.' * count
      else:
        text += '|' + (str(idx)+'.') * count + '|'
    return text

  def result(self):
    blocks = self.decompress(self.diskmap)
    print(Fore.YELLOW + self.str_debug(blocks) + Fore.RESET)
    blocks = self.super_defrag(blocks)
    print(Fore.GREEN + self.str_debug(blocks) + Fore.RESET)
    print(Fore.BLUE + 'Checksum:', self.checksum(blocks), Fore.RESET)

  def result1(self):
    blocks = self.decompress(self.diskmap)
    print(Fore.YELLOW + self.str_debug(blocks) + Fore.RESET)

    did, blocks = self.defrag(blocks)
    while did:
      #print(self.str_debug(blocks))
      did, blocks = self.defrag(blocks)
    print(Fore.GREEN + self.str_debug(blocks) + Fore.RESET)
    print(Fore.BLUE + 'Checksum:', self.checksum(blocks), Fore.RESET)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
