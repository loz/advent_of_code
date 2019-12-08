require "./src/puzzle"

puzzle = Puzzle.new
string = File.read("input")
puzzle.process(string, 25, 6)
puzzle.result
