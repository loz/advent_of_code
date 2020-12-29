class Puzzle:

  def process1(self, text):
    text = text.strip()
    self.value = 0
    last = ''
    for ch in text:
      if last == ch:
        self.value += int(ch)
      last = ch
    if text[0] == last:
      self.value += int(last)

  def process(self, text):
    text = text.strip()
    half = len(text) / 2
    text2 = text[half:] + text[0:half]
    self.value = 0
    for i in range(len(text)):
      ch1 = text[i]
      ch2 = text2[i]
      if ch1 == ch2:
        self.value += int(ch1)
       

  def result(self):
    print 'Value', self.value

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
