require 'ruby2d'

require_relative './particles'

particle_file = File.open("input")
#particle_file = File.open("input.example")
lines = particle_file.read

system = Particles.new
system.add_lines(lines)

bounds = system.bounds
puts "Bounds: %s" % bounds.inspect

vis_x = 640
vis_y = 480

set width: vis_x, height: vis_y

scale = system.scale_for(vis_x, vis_y)
puts "Scale for 640,480: %s" % scale.inspect 

offset = [0-bounds[0], 0-bounds[1]]
puts "Offset Origin: %s" % offset.inspect

set title: "Star System"

#system.particles.each do |particle|
#  puts particle.to_str
#end

def draw(particle, offset, scale)
  x = particle.x
  y = particle.y
  offset_x = x + (offset[0]) 
  offset_y = y + (offset[1])
  scale_x = offset_x * scale[0] * 0.5
  scale_y = offset_y * scale[1] * 0.5 
  scale_x += 100
  scale_y += 50

  Circle.new x: scale_x, y: scale_y, radius: 3
end

def calculate_offset(bounds)
 left, top, right, bottom = bounds
 [0-left, 0-top]
end

speed = 20
wait = 0
tick = 0
seconds = 0
update do
  clear
  system.particles.each do |particle|
    draw(particle, offset, scale)
  end
  system.move(speed)
  seconds += speed

  #Recalculate Bounds
  bounds = system.bounds
  #puts "Bounds: %s" % bounds.inspect
  scale = system.scale_for(vis_x, vis_y)
  #puts "Scale: %s" % scale.inspect
  offset = calculate_offset(bounds)
  #puts "Offset: %s" % offset.inspect
  #puts "Tick: %s" % tick
  tick += 1
  if tick == 500
    speed = 1
  elsif tick == 1000
    wait = 1
  elsif tick == 1015
    speed = 0
    puts "Stars Locked At Time Elapsed: %s" % seconds
  end
  sleep wait
end



show
