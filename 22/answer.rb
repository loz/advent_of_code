require_relative './cave'

cave = Cave.new(4845, [6,770])
puts "Cave risk: #{cave.total_risk}"
