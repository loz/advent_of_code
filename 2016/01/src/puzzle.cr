class Puzzle

  property orientation = "N"
  property location = {0,0}
  property visited = [] of Tuple(Int32,Int32)
 
  DIRECTIONS = {
    "N" => {
      "R" => {1, 0, "E"},
      "L" => {-1, 0, "W"}
    },
    "W" => {
      "R" => {0, -1, "N"},
      "L" => {0, 1, "S"}
    },
    "E" => {
      "R" => {0, 1, "S"},
      "L" => {0, -1, "N"}
    },
    "S" => {
      "R" => {-1, 0, "W"},
      "L" => {1, 0, "E"}
    }
  }

  def process(str)
    @visited << {0,0}
    str.split(", ").each do |move|
      apply(move)
    end
  end

  def apply(move)
    direction = move[0].to_s
    distance = move[1,move.size-1].to_i
    moves = DIRECTIONS[orientation][direction]
    dx, dy, neworientation = moves
    x, y = location
    @location = {x + (dx * distance), y + (dy * distance) }
    @orientation = neworientation
    if @visited.includes? location
      puts "Visited!: #{location}"
    else
      @visited << location
    end
  end

  def result
    puts "Walked"
    puts location
    puts orientation
  end

end
