a = 0
d = 12
b = 11
a = b * d
while b > 0:
  print a, b, d
  d = a
  b -= 1
  a = b * d

print 'Final', a, b, d
