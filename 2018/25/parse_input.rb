require_relative './constelation'

name = ARGV[0] || "input"

star_text = File.open(name) do |f|
  f.read
end
stars = Constelation.new 

star_text.each_line do |line|
  stars.add(line)
end
puts "Constelation Count: #{stars.constelations.count}"
