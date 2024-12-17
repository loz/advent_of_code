def machine_test(a, target):
  output = []
  while a != 0:
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
    #out: b % 8
    output.append(b % 8)
    #jze: 0
  print('O:', output)
  print('V:', target)

def machine(a, target):
  output = []
  while a != 0:
    b = a ^ 2
    c = a // (2^b)
    a = a // 8
    b = b ^ c
    b = b ^ 7
    output.append(b % 8)
    if target[:len(output)] != output:
      return False
  return (output == target)

target = [2,4,1,2,7,5,0,3,4,7,1,7,5,5,3,0]
a = 190384113204239
machine_test(a, target)
