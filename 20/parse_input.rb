require_relative './tree_map'

map_text = File.open("input") do |f|
  f.read
end
tree = TreeMap.build(map_text)
puts "Tree Depth: %s" % tree.depth
depths = tree.depths
puts "Tree Depths: %s" % depths.keys.count
puts " 1000+ doors: %s" % depths.count {|coord, d| d >= 1000 }
