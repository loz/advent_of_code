require "./intcode"

class VacuumRobot
  property image = [] of Array(Char)
  property curline = [] of Char
  property input = [] of Int64
  property lastch = '?'

  DELTA = {
    :N => { 0,-1},
    :S => { 0, 1},
    :E => { 1, 0},
    :W => {-1, 0}
  }

  TURN = {
    :N => {
      :W => "L",
      :E => "R",
      },
    :S => {
      :W => "R",
      :E => "L",
    },
    :E => {
      :N => "L",
      :S => "R",
    },
    :W => {
      :S => "L",
      :N => "R",
    }
  }

  def shift
    @input.shift
  end

  def <<(item)
    ch = item.chr

    #print ch
    case item
      when '\n'
        if @lastch == ch
          #print "\033[0;0f"
          @lastch = ""
        end
        @image << @curline
        @curline = [] of Char
      else
        @curline << ch
    end
    @lastch = ch
  end

  def locate_robot(screen)
    screen.each_with_index do |row, y|
      row.each_with_index do |ch, x|
        if ch == '^' 
          return {:N, {x,y}}
        end
      end
    end
    {:N, {-1,-1}} #Should not happen
  end

  def determine_turn(dir, pos, screen)
    neighbors = neighbors(pos, screen)
    option = neighbors.find do |n|
      newdir, ch = n
      ch == '#' && TURN[dir][newdir]?
    end
    if option
      newdir, _ = option
      turn = TURN[dir][newdir]
      return {newdir, turn}
    else
      return {:END, ""}
    end
  end

  def neighbors(pos, screen)
    maxy = screen.size - 1
    maxx = screen.first.size - 1
    neighbors = [] of Tuple(Symbol,Char)
    x,y = pos
    neighbors << {:N, screen[y-1][x]} unless y == 0
    neighbors << {:S, screen[y+1][x]} unless y == maxy
    neighbors << {:W, screen[y][x-1]} unless x == 0
    neighbors << {:E, screen[y][x+1]} unless x == maxx
    neighbors
  end

  def determine_distance(dir, pos, screen)
    maxy = screen.size - 1
    maxx = screen.first.size - 1
    delta = DELTA[dir]
    x, y = pos
    dx, dy = delta
    done = false
    distance = 0
    while !done 
      nx = x + dx
      ny = y + dy
      if nx < 0 || ny < 0 || nx > maxx || ny > maxy
        #Would exit map
        done = true
      else
        newchar = screen[ny][nx]
        if newchar == '#'
          x = nx
          y = ny
          distance += 1
        else
          done = true
        end
      end
    end
    {distance, {x,y}}
  end

  def build_route
    route = [] of String
    screen = (@image + [@curline]).reject {|l| l.empty? }

    loc = locate_robot(screen)
    dir, pos = loc
    while dir != :END
      turn = determine_turn(dir, pos, screen)
      dir, move = turn
      if dir != :END
        route << move
        dst, pos = determine_distance(dir, pos, screen)
        route << dst.to_s
      end
    end

    route
  end
  
  def render
    str = ""
    @image.each do |line|
      str += line.join
      str += '\n'
    end
    str += @curline.join
    str
  end

  def locate_intersections
    all = @image + [@curline]
    all = all.reject {|l| l.empty? }
    intersections = []  of Tuple(Int32,Int32)
    all.each_with_index do |row,y|
      row.each_with_index do |ch,x|
        next if x == 0 || y == 0
        next if x == row.size-1
        next if y == all.size-1
        if ch == '#'
          if all[y-1][x] == '#' &&
             all[y+1][x] == '#' &&
             all[y][x-1] == '#' &&
             all[y][x+1] == '#'
            intersections << {x,y}
            #print 'O'
          #else
            #print '#'
          end
        #else
          #print ch
        end
      end
      #print "\n:>"
    end
    intersections
  end

  def stringify(route)
    route.join(":") + ":"
  end

  def find_fn(route, upto)
    padroute = route + ",,,,"
    upto = [route.size, upto].min
    while upto > 0
      unless upto == route.size 
        while padroute[upto+2] != ',' && upto > 0
          upto -= 1
        end
      end

      poss = route[0,upto]
      if poss == route
        rest = ""
      else
        rest = route[upto+1, route.size]
      end

      if rest.includes? poss
        return {poss, rest}
      else
        upto -= 1
      end
    end
    {"", ""}
  end

  def do_zip(route)
    zip_function(route.join(","), 20)
  end

  def zip_function(route, upto, dict = [] of String, zipped = [] of Int32)
    return {dict, zipped} if route == ""
    if dict.size > 3
      return {[] of String, [] of Int32} 
    end
    #Try dictionary first
    dict.each_with_index do |seq, idx|
      if route == seq
        return {dict, zipped + [idx]}
      elsif route.starts_with?(seq)
        rest = route[seq.size+1, route.size]
        return zip_function(rest, 20, dict, zipped + [idx])
      end
    end
    upto.downto(1) do |n|
      fn, rest = find_fn(route, n)
      unless fn == ""
        idx = dict.size
        d, z = zip_function(rest, 20, dict + [fn], zipped + [idx])
        return {d,z} unless d.empty?
      end
    end
    return {[] of String, [] of Int32}
  end
end
