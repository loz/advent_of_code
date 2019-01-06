require_relative './recipe'

@recipe = Recipe.new
loc = 1
target = "157901"

puts "Searching for #{target}"
batch_size = 100_000

while (loc = @recipe.index_of(target)).nil?
  print "."
  batch_size.times { @recipe.run }
end
puts "Found: %s" % loc
