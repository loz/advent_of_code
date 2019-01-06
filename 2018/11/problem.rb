require_relative './power'

power = Power.new
serial = 3031

puts "Building Cells.."
power.build_cells(300,300,serial)
puts "Calculating Grids.."
300.times do |t|
  size = t+1
  print "%3d" % size
  print ":> "
  power.calculate_grids(size)
  x, y = power.largest_grid
  powerlevel = power.grid_power_at(x, y)
  print "%d @ (%d, %d)" % [powerlevel, x, y]
  puts
end

