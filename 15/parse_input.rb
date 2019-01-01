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

while !success do
  puts "\n" * 20
  puts "BIN SEARCH: #{worstap} -> #{bestap}                "
  attackpoints = ((bestap-worstap)/2)+worstap
  puts "Set Map.."
  battle.set_map(map)
  battle.visualise_map
  puts "Defining Targets.."
  battle.define_targets
  puts "Round: 0"
  puts "Fighting With #{attackpoints}.."
  puts "BIN SEARCH: #{worstap} -> #{bestap}                "
  battle.elves.each {|e| e.attack_points = attackpoints }

  puts "#{elves} Elves"
  success = worstap == bestap
  elfdied = false
  while battle.ongoing? do
    if battle.elves.count < elves
      puts "\n" * 20
      puts "Elf Died!"
      elfdied = true
      break
    end
    battle.turn
    battle.visualise_map
    puts ""
    puts "Battle Round: #{battle.round}, #{battle.elves.count} Elves.."
  end
  elfdied ||=  battle.elves.count < elves
  if elfdied
    #LOSE
    worstap = attackpoints + 1
  else
    #WIN
    bestap = attackpoints
  end
  sleep 1
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
