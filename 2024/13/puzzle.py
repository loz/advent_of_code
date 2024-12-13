import sys
import numpy as np
from colorama import Fore
from scipy.optimize import linprog
from pulp import LpProblem, LpVariable, LpMinimize, LpInteger, value, PULP_CBC_CMD

class Machine:

  def __str__(self):
    return str(self.a) + ':' + str(self.b) + '=>' + str(self.prize)
  
  def calculate_min_cost(self, debug=False, increase=0):
    """
      min 3a+b
      where:
        a*Ax + b*Bx = X
        a*Ay + b*By = Y
    """
    ax, ay = self.a
    bx, by = self.b
    tx, ty = self.prize

    tx += increase
    ty += increase

    matrix = np.array([[ax, bx], [ay, by]])
    prize = np.array([tx, ty])
    result = np.linalg.solve(matrix, prize).round()

    if all(matrix @ result == prize):
      return result @ [3, 1] 
    else:
      return 0


  def pulp_calculate_min_cost(self, debug=False, increase=0):
    """
      min 3a+b
      where:
        a*Ax + b*Bx = X
        a*Ay + b*By = Y
    """
    ax, ay = self.a
    bx, by = self.b
    tx, ty = self.prize

    tx += increase
    ty += increase

    problem = LpProblem("Integer_Linear_Programming", LpMinimize)

    a = LpVariable('a', cat=LpInteger)
    b = LpVariable('b', cat=LpInteger)

    problem += (3 * a) + b, 'Objective'

    problem += ((ax * a) + (bx * b)) == tx, 'Constraint1'
    problem += ((ay * a) + (by * b)) == ty, 'Constraint2'

    status = problem.solve(PULP_CBC_CMD(msg=0))

    if status == 1:
      return (value(a), value(b))
    else:
      return None


  def xxx_calculate_min_cost(self, debug=False, increase=0):
    """
      min 3a+b
      where:
        a*Ax + b*Bx = X
        a*Ay + b*By = Y
    """
    #print('Solving for:', self)
    ax, ay = self.a
    bx, by = self.b
    tx, ty = self.prize
    tx += increase
    ty += increase

    print('Solve:', ax, ay, ' ', bx, by, ' ', tx, ty)
    
    obj = [3, 1]

    lhs = [
      [ax, bx],
      [ay, by]
    ]

    rhs = [
      tx,
      ty
    ]

    #bnds = [(0, 100), (0, 100)]
    bnds = [(0, 100+(increase*increase)), (0, 100+(increase*increase))]

    opt = linprog(c=obj, A_eq=lhs, b_eq=rhs, integrality=[1,1], bounds=bnds, method='highs')
    #opt = linprog(c=obj, A_eq=lhs, b_eq=rhs, integrality=[1,1], method='highs')

    if opt.success:
      #print(opt)
      return (int(opt.x[0]), int(opt.x[1]))
    else:
      return None
    
  #def calculate_min_cost(self, debug=False):
  def x_calculate_min_cost(self, debug=False):
    """
      min 3a+b
      where:
        a*Ax + b*Bx = X
        a*Ay + b*By = Y
    """
    ax, ay = self.a
    bx, by = self.b
    tx, ty = self.prize
    values = {}
    costs = []
    for b in range(0, 100):
      if b * bx <= tx and b*by <= ty:
        remx = tx - (b*bx)
        remy = ty - (b*by)
        a  = remx // ax
        a2 = remy // ay
        if a == a2 and a*ax == remx:
          curcost = 3*a + b
          costs.append(curcost)
          values[curcost] = (a, b)
          print('a', a, 'b', b, 'cost', curcost)
    if costs:
      return values[min(costs)]
    else:
      return None

  def x_calculate_min_cost(self, debug=False):
    maxn = min(self.prize[0] // self.b[0], self.prize[1] // self.b[1])
    #if maxn > 100:
    #  print('This one is > 100')
    maxn = min(maxn, 100)

    best = None
    bestcost = None

    while maxn >= 0:
      #print('Max N:', maxn)
      remx = self.prize[0]-(self.b[0]*maxn)
      remy = self.prize[1]-(self.b[1]*maxn)

      mulx = remx // self.a[0]
      muly = remy // self.a[1]
      #if debug:
      #  isok = mulx == muly and (mulx * self.a[0] == remx)
      #  print('Try:', (mulx, maxn), '=>', 3*mulx+maxn, isok)
      #if mulx > 100:
      #  print('A press > 100')
      if mulx <= 100 and mulx == muly and (mulx * self.a[0] == remx):
        if debug:
          print('Found:', (mulx, maxn), '=>', 3*mulx+maxn)
        curcost = 3*mulx + maxn
        if best:
          if curcost < bestcost:
            best = (mulx, maxn)
            bestcost = curcost
        else:
          best = (mulx, maxn)
          bestcost = curcost
      maxn -= 1
    return best

class Puzzle:

  def process(self, text):
    self.machines = []
    for line in text.split('\n\n'):
      self.process_machine(line)

  def process_machine(self, chunk):
    if chunk != '':
      parts = chunk.split('\n')
      machine = Machine()
      #ASSUME A -> B -> PRIZE order
      machine.a = self.process_button(parts[0])
      machine.b = self.process_button(parts[1])
      machine.prize = self.process_prize(parts[2])
      self.machines.append(machine)

  def process_button(self, line):
    _, right = line.split(': ')
    x, y = right.split(',')
    _, x = x.split('+')
    _, y = y.split('+')
    return (int(x), int(y))

  def process_prize(self, line):
    _, right = line.split(': ')
    x, y = right.split(',')
    _, x = x.split('=')
    _, y = y.split('=')
    return (int(x), int(y))

  def result(self):
    totalcost = 0
    for m in self.machines:
      cost = m.calculate_min_cost(increase=10000000000000)
      if cost:
        #cash = 3*cost[0]+cost[1]
        #totalcost += cash
        #print(m, cost, cash)
        print(m, cost)
        totalcost += cost
      else:
        #print(m, cost, ' Not Possible ')
        print(m, ' Not Possible ')

    print('Total Cash:', totalcost)

  def result1(self):
    totalcost = 0
    for m in self.machines:
      cost = m.calculate_min_cost(True)
      if cost:
        cash = 3*cost[0]+cost[1]
        totalcost += cash
        print(m, cost, cash)
      else:
        print(m, cost, ' Not Possible ')
    print('Total Cash:', totalcost)

if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  print(Fore.GREEN + 'Processing:' + Fore.YELLOW + inputfile + Fore.RESET + '...')
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
