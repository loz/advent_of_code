require_relative './game'

print "405 players; last marble is worth 71700 points: "
game = Game.new
game.play(405, 71700)
puts " high score is #{game.highest_score}"
puts ""
print "405 players; last marble is worth 7170000 points: "
game = Game.new
game.play(405, 7170000)
puts "high score is #{game.highest_score}"
