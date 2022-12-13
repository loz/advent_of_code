a = b = c = d = e = f = g = h = 0
a = 1
b = 84 #set b 84
c = b #set c b
#jnz a 2
#jnz 1 5
b = b * 100 #mul b 100
b = b + 100000 #sub b -100000
c = b #set c b
c = c + 17000 #sub c -17000
f = 1
d = 2
e = 2

#set f 1  #FLoop
 #set d 2
 #set e 2 #ELoop
  #set g d #Gloop
while b <= c:
  f = False
  d = 2
  while not f and d < b: #((b/2)+1):
    if b % d == 0:  #this is the inner loop effectively
      f = True
      print 'Factor', d, b, '=', b/d
    d += 1
    #e = 2
    #while not f and e < ((b/2)+1):
    #  if d*e == b:
    #    f = True
    #    print 'Factor', d, e, b
    #  e += 1
    #  #g = d
    #   #mul g e
    #   #sub g b
    #   #jnz g 2 #If g == 0
    #   #set f 0 #DD
    #   #sub e -1 
    #   #set g e
    #   #sub g b
    #  #g = g * e
    #  #if g == b:
    #  #  f = 0
    #  #  break
    #  #g = e-b
    ##jnz g -8 Goto GLoop
    ##sub d -1
    ##set g d
    ##sub g b
    #print 'a', a, 'b', b, 'c', c, 'd', d, 'e', e, 'f', f, 'g', g, 'h', h
    #g = d - b
   #jnz g -13 Goto Eloop
  #jnz f 2
  #sub h -1
  if f:
    h += 1
  #print 'a', a, 'b', b, 'c', c, 'd', d, 'e', e, 'f', f, 'g', g, 'h', h
 #set g b
 #sub g c
  #g = b - c
  b += 17
print 'a', a, 'b', b, 'c', c, 'd', d, 'e', e, 'f', f, 'g', g, 'h', h

 #jnz g 2
 #jnz 1 3  #EXIT
 #sub b -17
#jnz 1 -23 Goto FLoop
