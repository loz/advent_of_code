require_relative './forrest'

forrest = Forrest.new
#vein_file = File.open("input.example")
tree_file = File.open("input")
trees = tree_file.read
forrest.set(trees)
puts "Starting Forrest:"
puts forrest.colorize(forrest.string)
puts "Value: %s" % forrest.value

seen = {}
#seen[0] = trees
468.times do |t|
  forrest.grow
  #string = forrest.string
  #if seen[string]
  #  puts "Repeat Found After #{seen[string]} -> #{t+1}"
  #  exit 1
  #end
  #seen[string] = t + 1
  #if t % 100 == 0
  #end
end
string = forrest.string
puts `clear`
puts "After 468 mins Forrest:"
puts forrest.colorize(string)
puts "Value: %s" % forrest.value

"
Repeat Found After 452 -> 480
480 == 452
481 == 453

target = 452 + ((ask - 452) % 28)
"

def calcgen(gen)
  452 + ((gen - 452) % 28)
end

puts "460 -> %s" % calcgen(460)
puts "452 -> %s" % calcgen(452)
puts "480 -> %s" % calcgen(480)
puts "481 -> %s" % calcgen(481)
puts "1_000_000_000 -> %s" % calcgen(1_000_000_000)
