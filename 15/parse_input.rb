require_relative './battle'

battle = Battle.new
map_file = File.open("input")
#map_file = File.open("input.stuck")
#map_file = File.open("input.example")
map = map_file.read

puts "Set Map.."
battle.set_map(map)


battle.visualise_map

puts "Defining Targets.."
battle.define_targets
puts "Fighting.."
while battle.ongoing? do
  battle.turn
  battle.visualise_map
  puts ""
  puts "Battle Round: #{battle.round}"
  #sleep 0.1
end

puts "Battle Finished @ #{battle.round}"

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
