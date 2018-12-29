require_relative './reservoir'

reservoir = Reservoir.new
#vein_file = File.open("input.example")
vein_file = File.open("input")
veins = vein_file.read
veins.each_line do |vein|
  reservoir.mark_vein(vein)
end

water = Water.new()
image = reservoir.visualise()
`open viz.png`
round = 0
#while !water.complete? do
30000.times do
  round += 1
  water.flow(reservoir)
  #if round % 1000 == 0
  #  puts "Rendering Round: #{round}"
  #  reservoir.visualise(image)
  #  `open viz.png`
  #end
end
reservoir.visualise(image)
`open viz.png`
puts "Totals:"
p reservoir.counts

#
#  round += 1
#  if round % 10 == 0
#    print "\e[0;0H"
#  end
#  #sleep 0.2
#end
