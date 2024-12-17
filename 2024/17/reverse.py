target = [2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0]

#Find last A which gives last digit
realA = 0
while target:
  print('-'*10)
  last = target.pop()
  print('A:', realA, 'v', last)
  for offset in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    ta = (realA * 8) + offset
    a = ta
    #bst: b = a % 8
    b = a % 8
    #bxl: b = b ^ 2
    b = b ^ 2
    #cdv: c = a // (2**b)
    c = a // (2**b)
    #adv: a = a // (2**3)
    a = a // (2**3)
    #bxl: b = b ^ c
    b = b ^ c
    #bxl: b = b ^ 7
    b = b ^ 7
    if (b % 8) == last:
      print(last, '-> A must have been', ta)
      realA = ta
      break



