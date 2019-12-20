alias Coord = Tuple(Int32,Int32)
alias State = Tuple(Int32, Coord)

class Puzzle

  DELTAS = [
    {-1, 0},
    { 1, 0},
    {0, -1},
    {0,  1}
  ]

  SURROUND = [
    {-1, 0},
    { 1, 0},
    {0, -1},
    {0,  1},
    {-1, -1},
    { 1,  1},
    {-1,  1},
    { 1, -1}
  ]

  property maze = [] of String
  property portals = {} of String => Array(Coord)
  property portal_map = {} of Coord => Coord
  property outer_corners = [] of Coord
  property inner_corners = [] of Coord

  def process(str)
    str.each_line do |line|
      process_line(line)
    end
    locate_portals
    map_portals
    find_corners
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
  
  def bounds(corners)
    cminx = @maze.first.size
    cmaxx = 0
    cminy = @maze.size
    cmaxy = 0
    corners.each do |c|
      x, y = c
      cminx = x if x < cminx
      cminy = y if y < cminy
      cmaxx = x if x > cmaxx
      cmaxy = y if y > cmaxy
    end
    [{cminx, cminy}, {cmaxx, cmaxy}]
  end

  def find_corners
    #For # spaces
    #Outer corners have *5* space/UPPER surrounding neighbors
    #Inner corners have *1* space/UPPER surrounding neighbor
    outers = [] of Coord
    inners = [] of Coord
    @maze.each_with_index do |row, y|
      row.each_char_with_index do |ch, x|
        if ch == '#'
          spaces = 0
          SURROUND.each do |delta|
            dx, dy = delta
            nx = x + dx
            ny = y + dy
            #p loc
            spaces += 1 if @maze[ny][nx] == ' '
            spaces += 1 if @maze[ny][nx].ascii_uppercase?
          end
          loc = {x, y}
          if spaces == 1
            inners << loc
          elsif spaces == 5
            outers << loc
          end
        end
      end
    end
    @outer_corners = bounds(outers) 
    @inner_corners = bounds(inners)
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

  def shortest_recursive_path(a,b)
    distances = { a => 0 }
    frontier = [ a ]
    while !frontier.empty?
      new_frontier = [] of State
      frontier.each do |loc|
        if loc == b #FOUND
          return distances[loc]
        end
        links = recursive_neighbors(loc)
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
    rstart = {0, start}
    rfinish = {0, finish}
    short = shortest_recursive_path(rstart, rfinish)
    puts "Recursive Shortest Path #{rstart} -> #{rfinish}: #{short}"
  end

  def internal_portal?(loc)
    top, bottom = inner_corners
    minx, miny = top
    maxx, maxy = bottom
    x, y = loc
    ((x == minx || x == maxx) && y >= miny && y <= maxy) ||
    ((y == miny || y == maxy) && x >= minx && x <= maxx)
  end

  def recursive_neighbors(state)
    level, loc = state
    shared = [] of State
    x, y = loc
    DELTAS.each do |delta|
      dx, dy = delta
      nx = x + dx
      ny = y + dy
      nloc = {nx, ny}
      cell = @maze[ny][nx]
      if cell == '.'
        shared << {level, nloc}
      end
    end
    if @portal_map[loc]?
      nloc = @portal_map[loc]
      if internal_portal?(loc)
        #Down a Level
        shared << {(level + 1), nloc}
      elsif level != 0
        #Up a Level, if not zero
        shared << {(level - 1), nloc}
      end
    end
    shared
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
