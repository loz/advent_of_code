require_relative './map'

map = Map.new
coord_file = File.open("input")
coords = coord_file.read
coords.each_line do |line|
  x, y = line.split(',')
  #puts "X: %s, Y: %s" % [x, y]
  map.add_point({x: x.to_i, y: y.to_i})
end

puts "Calculating Sums.."
map.calculate_distance_sums
print "Area Below 10,000: => "
puts map.sum_below(10_000)

puts "Calculating Grid.."
map.calculate_grid

puts "Calculating Areas.."
areas = map.calculate_areas
areas.each do |point, size|
  puts "Point: %s => %s" % [point.inspect, size]
end
