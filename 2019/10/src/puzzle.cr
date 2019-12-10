class Puzzle

  property rocks = {} of Tuple(Int32,Int32) => Bool

  def process(str)
    row = 0
    str.each_line do |line|
      #puts "#{row} -> #{line}"
      scan_row(row, line)
      row += 1
    end
  end

  def scan_row(y, line)
    line.each_char_with_index do |c, x|
      if c == '#'
        @rocks[{x, y}] = true
      end
    end
  end

  def line_of_sight?(from, to)
    p from, to
    points = points_between(from, to)
    p points
    points.each do |p|
      return false if @rocks[p]?
    end
    return true
  end
  
  def asteroids
    rocks.keys
  end

  def points_between(src, dest)
    locs = [] of Tuple(Int32, Int32)
    sc_x, sc_y = src
    ds_x, ds_y = dest

    dx = (ds_x - sc_x)
    dy = (ds_y - sc_y)
    p "Dx:#{dx}, Dy:#{dy}"
    if dx == 0
      (sc_y+1..ds_y-1).each do |y|
        locs << {sc_x, y}
      end
    elsif dy == 0
      (sc_x+1..ds_x-1).each do |x|
        locs << {x, sc_y}
      end
    else
      puts "----"
      d = if dx < 0
        -1
      else
        +1
      end
      x = sc_x + d
      while x != ds_x 
        xdy = x * dy
        if xdy % dx == 0
          y = (xdy / dx).to_i
          p({x,y})
          locs << {x, sc_y + y}
        end
        x = x + d
      end
    end
    locs
  end

  def result
  end

end
