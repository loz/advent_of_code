alias Coord = Tuple(Int32,Int32)

class Puzzle

  DELTAS = [
    {-1, 0},
    { 1, 0},
    {0, -1},
    {0,  1}
  ]

  property maze = [] of String
  property portals = {} of String => Array(Coord)
  property portal_map = {} of Coord => Coord

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
    locate_portals
    map_portals
  end

  def start
    portals["AA"].first
  end

  def finish
    portals["ZZ"].first
  end

  def process_line(line)
    @maze << line
  end

  def map_portals
    portals.each do |name, locs|
      next if locs.size != 2
      a, b = locs
      @portal_map[a] = b
      @portal_map[b] = a
    end
  end

  def add_portal(name, loc)
    if @portals[name]?
      @portals[name] << loc
    else
      @portals[name] = [loc]
    end
  end

  def locate_portals
    height = @maze.size
    width = @maze.first.size
    @maze.each_with_index do |row, y|
      next if y == 0
      next if y == (height-1)
      row.each_char_with_index do |ch, x|
        next if x == 0
        next if x == (width-1)
        if ch.ascii_uppercase?
          #ABOVE -> Below
          above = @maze[y-1][x]
          if above.ascii_uppercase?
            name = "#{above}#{ch}"
            loc = {x, y+1}
            add_portal(name, loc) if @maze[y+1][x] == '.'
          end
          #BELOW
          below = @maze[y+1][x]
          if below.ascii_uppercase?
            name = "#{ch}#{below}"
            loc = {x, y-1}
            add_portal(name, loc) if @maze[y-1][x] == '.'
          end
          #LEFT
          left = @maze[y][x-1]
          if left.ascii_uppercase?
            name = "#{left}#{ch}"
            loc = {x+1, y}
            add_portal(name, loc) if @maze[y][x+1] == '.'
          end
          #RIGHT
          right = @maze[y][x+1]
          if right.ascii_uppercase?
            name = "#{ch}#{right}"
            loc = {x-1, y}
            add_portal(name, loc) if @maze[y][x-1] == '.'
          end
        end
      end
    end
  end

  def shortest_path(a, b)
    distances = { a => 0 }
    frontier = [ a ]
    while !frontier.empty?
      new_frontier = [] of Coord
      frontier.each do |loc|
        links = neighbors(loc)
        links.each do |neighbor|
          next if distances[neighbor]? #Seen/Visited, Was Cheaper
          distances[neighbor] = distances[loc] + 1
          new_frontier << neighbor
        end
      end
      frontier = new_frontier
    end
    distances[b]
  end

  def result
    short = shortest_path(start, finish)
    puts "Shortest Path #{start} -> #{finish}: #{short}"
  end

  def neighbors(loc)
    shared = [] of Coord
    x, y = loc
    DELTAS.each do |delta|
      dx, dy = delta
      nx = x + dx
      ny = y + dy
      nloc = {nx, ny}
      cell = @maze[ny][nx]
      if cell == '.'
        shared << nloc
      end
    end
    if @portal_map[loc]?
      nloc = @portal_map[loc]
      shared << nloc
    end
    shared
  end
end
