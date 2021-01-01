class Puzzle:

  def process(self, text):
    self.phrases = []
    lines = text.split('\n')
    for line in lines:
      if line.strip() != '':
        self.phrases.append(line)

  def sort_letters(self, word):
    word = [ch for ch in word]
    word.sort()
    return ''.join(word)

  def valid(self, phrase):
    words = phrase.split()
    words = map(lambda x: self.sort_letters(x), words)
    return len(words) == len(set(words))

  def result(self):
    total = 0
    for phrase in self.phrases:
      isvalid = self.valid(phrase)
      print phrase, isvalid
      if isvalid:
         total += 1
    print 'Total Valid', total

if __name__ == '__main__':
  puz = Puzzle()
  inp = open('input', 'r').read()
  puz.process(inp)
  puz.result()
