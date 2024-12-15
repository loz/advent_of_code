from functools import reduce

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        print(a_i, '(mod', n_i,')')
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

n = [103, 101]
a = [50, 95]

print(chinese_remainder(n, a))

exit()
k=23
while True:
  n = -2250 + 101 * k
  m = 2295 + 103 * k

  t1 = 50+n * 103
  t2 = 95+m * 101

  if t1 == t2:
    print("Found:", t1)

  if k % 100000 == 0:
    print('k', k, 't', t1)
  k+=1 



n=50
n=103000000050
n=206000000050
for b in range(100):
  for i in range(10000000):
    n+= 103
    if (n-95)/101 == 0:
      print('Found', n)
      exit()
  print('@', n)
