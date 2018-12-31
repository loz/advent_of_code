require_relative './battle'

battle = Battle.new
#map_file = File.open("input")
map_file = File.open("input.example")
map = map_file.read

puts "Set Map.."
battle.set_map(map)

puts "Defining Targets.."
battle.define_targets

battle.units.each do |unit|
  unit.determine_range(battle.map)
  unit.filter_nearest(battle.map)
end
