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
while !water.complete? do
  round += 1
  water.flow(reservoir)
  if round % 100 == 0
    reservoir.visualise(image)
    `open viz.png`
  end
end

#
#  round += 1
#  if round % 10 == 0
#    print "\e[0;0H"
#  end
#  #sleep 0.2
#end
