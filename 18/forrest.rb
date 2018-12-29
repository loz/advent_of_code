COLORS = {
  "|" => "\e[92m|\e[0m",
  "#" => "\e[91m#\e[0m",
}

LOCS = [
  [-1, -1],
  [-1,  0],
  [-1,  1],
  [ 0, -1],
  [ 0,  1],
  [ 1, -1],
  [ 1,  0],
  [ 1,  1]
]

class Forrest
  def set(string)
    @current = string.lines.map &:chomp
    @next = string.lines.map &:chomp
    @width = @current.first.length
    @height = @current.count
  end

  def value
    trees = 0
    lumber = 0
    @current.each do |row|
      row.each_char do |cell|
        trees += 1 if cell == '|'
        lumber += 1 if cell == '#'
      end
    end
    trees * lumber
  end

  def grow
    #puts "****** GROWING *****"
    #  puts colorize(string)
    #puts "vvvvvvvvvvvvvvvvvvvv"
    @current.each_with_index do |row, y|
      @width.times do |x|
        #print "Adjacent to %s, %s >> " % [x,y]
        locs = LOCS.map {|l| [x + l[0], y + l[1]]}
        locs.reject! do |loc|
          lx, ly = loc
          lx < 0 ||
          ly < 0 ||
          lx == @width ||
          ly == @height
        end
        adjacent = locs.map do |loc|
          ax, ay = loc
          @current[ay][ax]
        end
        grow_cell(x,y,adjacent)
        #p adjacent
      end
    end
    last = @current
    @current = @next
    @next = last
  end

  def colorize(string)
    COLORS.each do |k,v|
      string = string.gsub(k, v)
    end
    string
  end

  def string
    @current.join("\n") + "\n"
  end

  private

  def grow_cell(x, y, adjacent)
    cell = @current[y][x]
    trees = adjacent.count {|c| c == "|"}
    lumber = adjacent.count {|c| c == "#" }
    if cell == "."
      if trees >= 3
        @next[y][x] = "|"
      else
        @next[y][x] = "."
      end
    elsif cell == "|"
      if lumber >= 3
        @next[y][x] = "#"
      else
        @next[y][x] = "|"
      end
    elsif cell == "#"
      if trees < 1 || lumber < 1
        @next[y][x] = "."
      else
        @next[y][x] = "#"
      end
    end
  end
end
