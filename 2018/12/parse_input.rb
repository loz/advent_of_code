require_relative './plants'

notes_file = File.open("input")
lines  = notes_file.read

plants = Plants.from_lines(lines)
puts "-- Growing --"
#10_000_000.times do |t|
110.times do |t|
  plants.grow
  if t % 1 == 0
   puts t
   plants.dump  
  end
end
puts "--------"

additional = (50_000_000_000 - 108) * 65
final = 7976 + additional

puts "Final Score after 50B: #{final}"

