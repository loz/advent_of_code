require_relative './checksum'

checksum = Checksum.new
boxcode_file = File.open("input")
string = boxcode_file.read
puts "Matches Are: ", checksum.search(string)
