require_relative './battle'

battle = Battle.new
map_file = File.open("input")
map = map_file.read

puts "Set Map.."
battle.set_map(map)

puts "Defining Targets.."
battle.define_targets
battle.visualise_map
battle.elves.each do |elf|
  elf.determine_range(battle.map)
  elf.filter_reachable(battle.map)
  elf.filter_nearest(battle.map)
  battle.visualise_locations(elf.locations, :yellow)
end
battle.goblins.each do |goblin|
  goblin.determine_range(battle.map)
  goblin.filter_reachable(battle.map)
  goblin.filter_nearest(battle.map)
  battle.visualise_locations(goblin.locations, :green)
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
