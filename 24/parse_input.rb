require_relative './immune'

group_text = File.open("input") do |f|
#group_text = File.open("input.example") do |f|
  f.read
end
system = Immune.new 
@good = []
@bad = []

group_text.each_line do |line|
  case line
  when "Immune System:\n"
    puts "Parsing Immune"
    @current = @good
  when "Infection:\n"
    puts "Parsing Infection"
    @current = @bad
  when "\n"
  else
    @current << system.parse_group(line)
  end
end

system.good = @good
system.bad = @bad
puts "Good Groups:"
@good.each do |group|
  weak = group.weaknesses.map {|w| w.inspect }
  immune = group.immunity.map {|w| w.inspect }
  puts "#{group.name} #{group.damage.inspect.inspect} I:#{immune} W:#{weak}"
end
puts "Bad Groups:"
@bad.each do |group|
  weak = group.weaknesses.map {|w| w.inspect }
  immune = group.immunity.map {|w| w.inspect }
  puts "#{group.name} #{group.damage.inspect.inspect} I:#{immune} W:#{weak}"
end

#exit

lower = 0
upper = 2 ** 20
lower = 35
upper = 36
bestscore = nil

stalemates = [32,33,34]

while lower != upper do
#22.times do
  boost = lower + ((upper-lower)/2)
  puts ""
  puts "-"*20
  puts "Boost: #{boost}  [#{lower}..#{upper}]"
  boosted = @good.map { |g| g = g.dup; g.damage_points+=boost; g }
  baddies = @bad.map { |g| g = g.dup }
  system.good = boosted
  system.bad = baddies

  puts "."*20
  puts "Good Groups:"
  system.good.each do |group|
    puts "#{group.name} #{group.damage_points}"
  end
  puts "Bad Groups:"
  system.bad.each do |group|
    puts "#{group.name} #{group.damage_points}"
  end
  puts "."*20
  puts "Fighting!"
  while !system.good.empty? && !system.bad.empty? do
  #10.times do
    #puts "Good (%s) v Bad (%s)" % [system.good.count, system.bad.count]
    #print "."
    #system.dump
    system.fight!
  end
  puts ""
  puts "Battle Ended"
  if system.good.empty?
    lower = boost
    if boost+1 == upper
      lower = upper
    end
    puts "Bad Won: %s units left in total" % system.bad.inject(0) {|s,g| s+=g.units }
  else
    upper = boost
    bestscore = system.good.inject(0) {|s,g| s+=g.units }
    puts "Good Won: %s units left in total" % bestscore
  end
end
puts "*"*20
puts "Best Boost: #{upper}"
puts "Total Units: #{bestscore}"
