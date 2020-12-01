import itertools

class Puzzle:

  def process(this, text):
    this.nums = map(lambda n: int(n), text.split())

  def sum(this, target):
    comb = itertools.combinations(this.nums, 2)
    for pair in comb:
      a, b = pair
      if (a+b) == target:
        return pair

  def sum3(this, target):
    comb = itertools.combinations(this.nums, 3)
    for pair in comb:
      a, b, c = pair
      if (a+b+c) == target:
        return pair

  def result(this):
    pair = this.sum3(2020)
    print(pair)
    a, b, c = pair
    print("*=", a*b*c)

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
