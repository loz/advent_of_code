import sys
from colorama import Fore
from collections import Counter

class Puzzle:

  def __init__(self):
    self.numbers = []
    self.sequences = Counter()


  def process(self, text):
    for line in text.split('\n'):
      self.process_line(line)

  """
Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
  """
  def generate(self, n):
    #Calculate the result of multiplying the secret number by 64.
    r = n * 64
    #  Then, mix this result into the secret number.
    n = n ^ r
    #  Finally, prune the secret number.
    n = n % 16777216

    # Calculate the result of dividing the secret number by 32.
    #   Round the result down to the nearest integer.
    r = n // 32
    #   Then, mix this result into the secret number.
    n = n ^ r
    #   Finally, prune the secret number.
    n = n % 16777216

    # Calculate the result of multiplying the secret number by 2048.
    r = n * 2048
    #   Then, mix this result into the secret number.
    n = n ^ r
    #   Finally, prune the secret number.
    n = n % 16777216
    return n
  
  def generate_n(self, num, n):
    for i in range(n):
      num = self.generate(num)
    return num

  def sequence(self, key):
    return self.sequences[key]

  def count_sequences(self, num, n):
    onum = num
    last = num % 10
    window = []
    seen = {}
    for i in range(n):
      num = self.generate(num)
      d = num % 10
      delta = d - last
      window.append(delta)
      if len(window) == 4:
        #print(window, d)
        seq = tuple(window)
        #if seq == (-2, 1, -1, 3):
        #  print('See', seq, 'in', onum, 'd=', d, flush=True)
        if seq not in seen:
          seen[seq] = True
          self.sequences[seq] += d
        window.pop(0)
      last = d

  def process_line(self, line):
    if line != '':
      self.numbers.append( int(line) )

  def result(self):
    #self.resultspecific()
    self.result2()

  def resultspecific(self):
    self.count_sequences(2, 2000)


  def result2(self):
    for num in self.numbers:
      self.count_sequences(num, 2000)
    print(self.sequences.most_common(1))

  def result1(self):
    total = 0
    for num in self.numbers:
      res = self.generate_n(num, 2000)
      print(num, ':', res)
      total += res
    print('Total:', total)


if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
