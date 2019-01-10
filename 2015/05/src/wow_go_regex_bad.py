import re


def is_nice(string):
  banned = re.search(r'(ab|cd|pq|xy)', string) != None
  if banned:
    return False 
  repeats = re.search(r'(\w)\1+', string) != None
  vowels = re.search(r'(.*[aeiou].*){3}', string) != None
  return vowels & repeats

def is_new_nice(string):
  pairs = re.search(r'(\w\w).*\1+', string) != None
  repeats = re.search(r'(\w).\1+', string) != None
  return pairs & repeats

with open('input.txt', 'r') as f:
  lines = f.read()
f.closed


print "qjhvhtzxzqqjkmpb IS", is_new_nice("qjhvhtzxzqqjkmpb")
print "xxyxx IS", is_new_nice("xxyxx")
print "uurcxstgmygtbstg IS", is_new_nice("uurcxstgmygtbstg")
print "ieodomkazucvgmuy IS", is_new_nice("ieodomkazucvgmuy")

count = 0
for line in lines.splitlines():
  nice = is_new_nice(line)
  if nice:
    count += 1
  print line, " => ", nice

print "Total Nice: ", count
