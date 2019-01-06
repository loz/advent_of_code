require_relative './polymer'

polymer = Polymer.new
chain_file = File.open("input")
original = chain_file.read.chomp
('a'..'z').each do |letter|
  print "Removing #{letter}:> "
  chain = original.delete letter
  chain = chain.delete letter.upcase
  newchain = polymer.trigger(chain)
  puts newchain.length
end
