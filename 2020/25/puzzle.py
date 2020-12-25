class Puzzle:

  def calcloop(self, pubkey, subject):
    val = 1
    num = 0
    while val != pubkey:
      val = val * subject
      val = val % 20201227
      num +=1
    return num

  def encode(self, subject, privkey):
    val = 1
    for i in range(privkey):
      val = val * subject
      val = val % 20201227
    return val

  def result(self):
    pubkey1 = 10943862
    pubkey2 = 12721030
    privkey1 = self.calcloop(pubkey1, 7)
    privkey2 = self.calcloop(pubkey2, 7)
    print 'Pub1:', pubkey1, 'Priv:', privkey1
    print 'Pub2:', pubkey2, 'Priv:', privkey2
    enckey = self.encode(pubkey1, privkey2)
    print 'Encryption Key:', enckey

if __name__ == '__main__':
  puz = Puzzle()
  puz.result()
