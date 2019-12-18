class Puzzle
  alias Coord = Tuple(Int32,Int32)
  alias State = Tuple(Coord, Array(Char))

  DELTAS = [
    {-1, 0},
    { 1, 0},
    {0, -1},
    {0,  1}
  ]
  
  property maze = [] of Array(Char)
  property start = {0,0}
  property spaces = 0

  def process(str)
    str.lines.each do |line|
      process_line(line)
    end
    analyse
    @curpos = @start
  end

  def neighbors(state)
    curpos, keys = state
    x, y = curpos
    states = [] of State
    DELTAS.each do |delta|
      dy, dx = delta
      nx = x + dx
      ny = y + dy
      ch = at(nx, ny)
      if can_visit?(nx, ny, keys)
        if ch.ascii_lowercase?
          states << { {nx, ny}, keys + [ch] }
        else
          states << { {nx, ny}, keys }
        end
      end
    end
    states
  end

  def can_visit?(x,y, keys)
    cell = at(x,y)
    if cell == '#'
      false
    elsif cell.ascii_uppercase?
      key = cell.downcase
      if keys.includes?(key)
        return true
      else
        return false
      end
    else
      return true
    end
  end

  def new_candidates(state)
    neighbors(state)
  end

  def analyse
    @maze.each_with_index do |row, y|
      row.each_with_index do |ch, x|
        @start = {x,y} if ch == '@'
        @spaces += 1 if ch != '#'
      end
    end
  end

  def process_line(line)
    @maze << line.chomp.chars
  end

  def at(x,y)
    @maze[y][x]
  end

  def explore
    keys = [] of Char
    frontier = [{start, keys}]
    distances = {} State => Int33

    3.times do
    if frontier.any?
      new_frontier = [] of State
      frontier.each do |state|
        states = neighbors(state)
        p states
      end
    end
    end
    p frontier
  end

  def result
    explore
  end

end
