require "./src/puzzle"

puzzle = Puzzle.new
string = File.read("input")
puzzle.process(string)
puzzle.result
