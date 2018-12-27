require_relative './reservoir'

reservoir = Reservoir.new
#vein_file = File.open("input.example")
vein_file = File.open("input")
veins = vein_file.read
veins.each_line do |vein|
  reservoir.mark_vein(vein)
end

water = Water.new()
puts `clear`
reservoir.visualise
round = 0
while !water.complete? do
  round += 1
  water.flow(reservoir)
  if round % 10 == 0
    print "\e[0;0H"
    reservoir.visualise
  end
  #sleep 0.2
end
