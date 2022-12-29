require_relative './battle'

battle = Battle.new
map_file = File.open("input")
#map_file = File.open("input.stuck")
#map_file = File.open("input.example")
#map_file = File.open("input.3")
map = map_file.read

worstap = 3
bestap = 101
success = false
attackpoints = bestap
battle.set_map(map)
elves = battle.elves.count
while battle.ongoing? do
  battle.turn
  battle.visualise_map
  puts ""
  puts "Battle Round: #{battle.round}, #{battle.elves.count} Elves.."
  hitpoints = 0
  battle.elves.each do |u|
    if u.hitpoints >0
      hitpoints += u.hitpoints
    end
  end
  puts "Elves: #{hitpoints}     "
  hitpoints = 0
  battle.goblins.each do |u|
    if u.hitpoints >0
      hitpoints += u.hitpoints
    end
  end
  puts "Goblins: #{hitpoints}     "
  if battle.round > 77
    puts "Press ENTER to continue......."
    gets 
  end
end
puts "Battle Finished @ #{battle.round}"
hitpoints = 0
battle.units.each do |u|
  hitpoints += u.hitpoints
end
puts "Hitpoints: #{hitpoints}"
puts "Score: #{hitpoints * battle.round }"
puts "Elf Attack: #{attackpoints}"

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
