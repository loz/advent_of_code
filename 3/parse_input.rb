require_relative './fabric'

fabric = Fabric.new
claim_file = File.open("input")
lines = claim_file.read
fabric.apply_claims(lines)
#puts "Overlaps Are: ", fabric.overlapping_squares
puts "Finding Unshared Claims"
puts fabric.find_unshared_claims
