running = true
while running
  ch = gets('\n',1)
  puts ch
  running == !(ch == '\n')
end
