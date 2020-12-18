import re

TOKENS=r"(\d+|[\+\*\-\/\(\)])"

PREC = {
  "+": 3,
  "*": 2,
  "(": 1
}

class Puzzle:

  def process(self, text):
    lines = text.split('\n')
    self.results = []
    for line in lines:
      if line.strip() != '':
        self.results.append(self.eval(line))

  def eval(self, line):
    tokens = self.tokenise(line)
    tokens = self.build_postfix(tokens)
    print tokens
    return self.consume(tokens)

  def build_postfix(self, tokens):
    #print 'TOKENS:', tokens
    opstack = []
    output = []
    for token in tokens:
      if token == '(':
        opstack.append(token)
      elif token == ')':
        while len(opstack) != 0 and opstack[len(opstack)-1] != '(':
          op = opstack.pop()
          output.append(op)
        opstack.pop() #remove matching ')'
      elif token == '+' or token == '*':
        while len(opstack) != 0 and PREC[opstack[len(opstack)-1]] >= PREC[token]:
          op = opstack.pop()
          output.append(op)
        opstack.append(token)
      else:
        output.append(int(token))
    #Finally clear opstack
    while len(opstack) > 0:
      op = opstack.pop()
      output.append(op)
    #print 'POSTFIX:', output
    return output
  
  def consume(self, tokens):
    stack = []
    for token in tokens:
      #print token, stack
      if token == '+':
        rhs = stack.pop()
        lhs = stack.pop()
        stack.append(rhs + lhs)
      elif token == '*':
        rhs = stack.pop()
        lhs = stack.pop()
        stack.append(rhs * lhs)
      else:
        stack.append(token)
    
    return stack[0]

  def tokenise(self, line):
    print "LINE:", line
    matches = re.findall(TOKENS, line)
    return matches

  def result(self):
    total = 0
    for res in self.results:
      print res
      total += res
    print 'SUM', total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
