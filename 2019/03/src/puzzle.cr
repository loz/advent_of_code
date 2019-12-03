class Puzzle
  property grid = [] of String
  property startx = 0
  property starty = 0
  property intersections = [] of Tuple(Int32,Int32)

  def process(str)
    first = str.lines[0]
    second = str.lines[1]
    b1 = bounds(first)
    b2 = bounds(second)
    minx = [b1[0], b2[0]].min
    miny = [b1[1], b2[1]].min
    maxx = [b1[2], b2[2]].max
    maxy = [b1[3], b2[3]].max
    bounds = {minx,miny,maxx,maxy}
    init_grid(bounds)
    plot(first, '1')
    plot(second, '2')
  end

  def closest_intersection
    @intersections.min_by do |loc|
      distance_to(loc)
    end
  end

  def distance_to(loc)
    loc[0].abs + loc[1].abs
  end

  def plot_at(x,y, marker)
    e = get(x, y)
    if e != '.' && e != marker
      set(x, y, 'X')
      @intersections << {x-startx,y-starty}
    else 
      set(x, y, marker)
    end
  end

  def plot(seq, marker)
    curx = startx
    cury = starty
    seq.split(",").each do |move|
      direction, distance = parse(move)
      case direction
        when 'R'
          distance.times do
            curx += 1
            plot_at(curx,cury,marker)
          end
        when 'L'
          distance.times do
            curx -= 1
            plot_at(curx,cury,marker)
          end
        when 'U'
          distance.times do
            cury += 1
            plot_at(curx,cury,marker)
          end
        when 'D'
          distance.times do
            cury -= 1
            plot_at(curx,cury,marker)
          end
      end
    end
  end

  def set(x,y,char)
    @grid[y] = @grid[y].sub(x, char)
  end

  def get(x,y)
    @grid[y].char_at(x)
  end

  def to_s
    grid.reverse.join("\n")
  end

  def init_grid(bounds)
    minx, miny, maxx, maxy = bounds
    width = (minx-maxx).abs + 1
    height = (miny-maxy).abs + 1
    height.times do |y|
      @grid << ("." * width)
    end
    @startx = 0-minx
    @starty = 0-miny
    set(startx, starty, 'o')
  end

  def parse(move)
    {move[0], move[1,move.size].to_i}
  end

  def bounds(seq)
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    curx = 0
    cury = 0
    seq.split(",").each do |move|
      direction, distance = parse(move)
      case direction
        when 'R'
          curx += distance
        when 'L'
          curx -= distance
        when 'U'
          cury += distance
        when 'D'
          cury -= distance
      end
      maxx = curx if curx > maxx
      maxy = cury if cury > maxy
      minx = curx if curx < minx
      miny = cury if cury < miny
    end
    {minx, miny, maxx, maxy}
  end

  def result
    closest = closest_intersection
    puts "Closest: #{closest}"
    puts distance_to(closest)
  end

end
