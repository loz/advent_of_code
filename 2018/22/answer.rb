require_relative './cave'

start = [[0,0], :torch]
target = [[6,770], :torch]

cave = Cave.new(4845, [6,770])
puts "Cave risk: #{cave.total_risk}"
route = cave.navigate(start, target)
puts "Shortest Route: #{cave.cost(route)}"
