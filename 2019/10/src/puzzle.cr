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
    points = points_between(from, to)
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

    dlx = dx.abs
    dly = dy.abs

    drx = dx < 0 ? -1 : 1
    dry = dy < 0 ? -1 : 1

    #p "Dx:#{dx}, Dy:#{dy}"
    if dx == 0
      (1..dly-1).each do |y|
        locs << {sc_x, sc_y + (y*dry)}
      end
    elsif dy == 0
      (1..dlx-1).each do |x|
        locs << {sc_x + (x*drx), sc_y}
      end
    else
      #puts "----"
      (1..dlx-1).each do |x|
        xdy = x * dy
        if xdy % dx == 0
          y = (xdy / dx).to_i
          nx = sc_x + (x*drx)
          ny = sc_y + (y*dry)
          locs << {nx, ny}
        end
      end
    end
    locs
  end

  def result
  end

end
