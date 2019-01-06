require_relative './tree'

tree = Tree.new
key_file = File.open("input")
key = key_file.read

tree.from_key(key)
puts "Checksum: #{tree.checksum}"
puts "Value: #{tree.value}"
