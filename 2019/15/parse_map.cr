require "./src/diffuse"

map = Diffuse.new
string = File.read("map.txt")
map.process(string)
map.result
