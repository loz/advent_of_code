import sys
import itertools
import numpy as np
import sympy

class Puzzle:

  def process(self, text):
    self.hailstones = []
    for line in text.split('\n'):
      self.process_line(line)

  def process_line(self, line):
    if line != '':
      line = line.replace(' @', ',')
      parts = [int(n) for n in line.split(', ')]
      x, y, z, vx, vy, vz = parts
      p = (x, y, z)
      v = (vx, vy, vz)
      self.hailstones.append((p, v))
  """
  Hailstone A: 19, 13, 30 @ -2, 1, -2
  Hailstone B: 18, 19, 22 @ -1, -1, -2
  Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

  ax+t1*avx
  (14.333 - 19) / -2 -> t1 -> 2.333
  bx+t2*avx
  (14.33 - 18) / -1 -> t2 > 3.67
  T DOES NOT HAVE TO BE THE SAME! JUST WHEN LINES CROSS

"""

  def coefficients(self, p, v):
    (x, y, z) = p
    (vx, vy, vz) = v

    a = (vx / vz)
    b = (vy / vz)
    c = (z - a) * (x - b) * y
    return a, b, c


  def paths_cross(self, a, b):
    #Estimating only XY
    # x1 = a_x+t*a_vx
    # x2 = b_x+t*b_vx
    # y1 = a_y+t*a_vy
    # y2 = b_y+y*b_vy
    # collide if: ax+t*avx == bx+t*bvx
    #        and: ay+t*avy == by+t*bvy
    # => t = (bx-ax)/(avx-bvx)
    # => plug t back into equation
    (ax, ay, _), (avx, avy, _) = a
    (bx, by, _), (bvx, bvy, _) = b

    ma = avy / avx
    mb = bvy / bvx

    if ma == mb:
      return None

    c_a = ay - ma * ax
    c_b = by - mb * bx

    x = (c_b - c_a) / (ma - mb)
    #y = mx + c
    y = ma * x + c_a

    ta = (x - ax) / avx
    tb = (x - bx) / bvx

    return ((x, y), (ta, tb))

  def collide(self, p, v, coef):
    pa, pb, pc = self.coefficients(p, v)
    la, lb, lc = coef
    #print('P:', (pa, pb, pc), 'L:', (la, lb, lc))

    A = np.array([[pa, pb], [la, lb]])
    b = np.array([-pc, -lc])

    # Solve for x and y
    x, y = np.linalg.solve(A, b)

    # Calculate z using either of the original equations
    z = (pa * x) + (pb * y) + pc
    

    px, py, pz = p
    vx, vy, vz = v
    # x = px + t * vx
    # x-px = t * vx
    # (x-px) / vx = t
    #t = (x-px) / vx
    #t2 = (y-px) / vy
    t = (z-pz) / vz
    #print("Intersect ", (x, y, z), '@', t, t2, t3)
    return ((x, y, z), t)
    

  def result(self):
    self.result2()

  def result2(self):
    #Want rx, ry, rz, rvx, rvy, rvz
    #Have MANY:
    #    x, y, z, vx, vy, vz
    """
      x + t*vx = rx + t*rvx => t = (rx - x) / (vx - rvx)
      y + t*vy = ry + t*rvy => t = (ry - y) / (vy - rvy)
      z + t*vz = rz + t*rvz => t = (rz - z) / (vz - rvz)

      t must be same for all, so solve r varaibles for
      (rx - x) / (vx - rvx) = (ry - y) / (vy - rvy) = (rz - z) / (vz - rvz)
    """
    rx, ry, rz, rvx, rvy, rvz = sympy.symbols("rx, ry, rz, rvx, rvy, rvz")
    equations = []
    for h in self.hailstones[0:10]:
      (x, y, z), (vx, vy, vz) = h
      equations.append((rx - x) / (vx - rvx) - (ry - y) / (vy - rvy))
      equations.append((ry - y) / (vy - rvy) - (rz - z) / (vz - rvz))
    answer = sympy.solve(equations)[0]
    print(answer)
    print('Solution:', answer[rx]+answer[ry]+answer[rz])


  def result2_manual(self):
    lines = []
    for h in self.hailstones:
      p, v = h
      a, b, c = self.coefficients(p, v)
      lines.append([a, b, c])
      #print(p, v, '=>', a, b, c)
    lines = np.array(lines)
    
    A = lines[:, :-1] 
    b = -lines[:, -1]

    A= np.column_stack((A, np.ones(len(lines))))

    result, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    a, b, c = result[:3]
    print('Equation of line: z = ax + by + c', a, b, c)
    for h in self.hailstones:
      p, v = h
      t = self.collide(p, v, (a, b, c))
      print(p, v, t)


  def inbounds(self, bounds, v):
    return v >= bounds[0] and v <= bounds[1]

  def result1(self):
    pairs = itertools.combinations(self.hailstones, 2)
    #bounds = (7, 27)
    bounds = (200000000000000, 400000000000000)
    total = 0
    for a, b in pairs:
      c = self.paths_cross(a,b)
      if c == None:
        print(a, b, c)
      else:
        (x, y), (ta, tb) = c
        if ta < 0 and tb < 0:
          print(a, b, 'in past for A and B')
        elif ta < 0:
          print(a, b, 'in past for A')
        elif tb < 0:
          print(a, b, 'in past for B')
        elif self.inbounds(bounds, x) and self.inbounds(bounds, y):
          print(a, b, 'cross INSIDE, at',  (x,y))
          total += 1
        else:
          print(a, b, 'out of bounds, at', (x, y))
    print('Total', total)



if __name__ == '__main__':
  puz = Puzzle()
  inputfile = 'input'
  if len(sys.argv) == 2:
    inputfile = sys.argv[1]
  inp = open(inputfile, 'r').read()
  puz.process(inp)
  puz.result()
