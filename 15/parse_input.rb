require_relative './battle'

battle = Battle.new
map_file = File.open("input")
#map_file = File.open("input.example")
map = map_file.read

puts "Set Map.."
battle.set_map(map)

puts "Defining Targets.."
battle.define_targets

while true do
  battle.turn
end

=begin
elf = battle.elves[0]
puts "Detemining Range.."
elf.determine_range(battle.map)
puts "Reachable.."
battle.visualise_map
battle.visualise_locations(elf.locations)
elf.filter_reachable(battle.map)
puts "Nearest.."
battle.visualise_map
battle.visualise_locations(elf.locations)
elf.filter_nearest(battle.map)
puts "Visualising.."
battle.visualise_map
battle.visualise_locations(elf.locations)
=end
